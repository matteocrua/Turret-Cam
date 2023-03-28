# import functions from other files
from flask import Flask, render_template, request, redirect, Response, send_file
from picamera import PiCamera
from io import BytesIO
from Turret import *
# library imports
import numpy as np
import cv2
import functions
from PIL import Image

# initialize the camera width and height
FRAME_WIDTH = 640
FRAME_HEIGHT = 368

app = Flask(__name__)

# home page for turret cam
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/controls', methods = ['POST', 'GET'])
def controls():
    if request.method == 'POST': 
        form_data = request.form
        functions.parse_user_input(form_data['control'])
        #print(form_data['control'])
        #print(functions.face_tracking)
        return "Success", 201
    else:
        # prevent access to /data => redirect to root
        return redirect("/")

@app.route('/speed', methods = ['POST', 'GET'])
def speed_mult():
    if request.method == 'POST':
        form_data = request.form
        functions.kp_multiplier(float(form_data['speed']))
        #print(form_data['speed'])
        return "Success", 201
    else:
        # The URL /data/ is accessed directly so redirect to root.
        return redirect("/")
    
@app.route('/snapshot', methods=['POST'])
def snapshot():
    # Capture a frame from the Picamera
    stream = BytesIO()
    camera.capture(stream, format='jpeg')
    stream.seek(0)

    # Open the frame as a PIL image
    image = Image.open(stream)

    # Flip the image horizontally and vertically
    flipped = image.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)

    # Save the flipped image to a new stream
    flipped_stream = BytesIO()
    flipped.save(flipped_stream, 'jpeg')
    flipped_stream.seek(0)

    # Send the flipped image as a download to the user
    return Response(
        flipped_stream,
        mimetype='image/jpeg',
        headers={
            'Content-Disposition': 'attachment; filename=snap.jpg'
        }
    )

@app.route('/record', methods=['POST'])
def record():
    # Get the video duration from the request
    duration = int(request.form['duration'])

    # Create a BytesIO object to hold the video data
    video_stream = BytesIO()

    # Initialize the camera and start recording
    camera.start_recording(video_stream, format='mjpeg')

    # Wait for the specified duration
    time.sleep(duration)

    # Stop recording and close the camera
    camera.stop_recording()
    #camera.close()

    # Send the video file to the client for download
    video_stream.seek(0)
    return send_file(video_stream, download_name='video.mjpeg', as_attachment=True)

@app.route('/video')
def video():
    # /video endpoint
    # provides a webcam video feed that can be used in a source for an <img> ta
    # prevent direct access to /video by checking that the referrer is the host 
    if request.headers.get("Referer") == request.host_url:
        # generate video feed, mimetype tells the browser what data to expect
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        # referer unknown => redirect to root
        return redirect("/")
    
# infinite loop to continuously stream jpeg frames
def generate_frames():
    # np.empty creates an empty array of the specified size and type 
    # uint8 is an 8-bit unsigned integer (0 to 255) 
    # the array is 1D and the size is the number of pixels in the frame
    # 3 is the number of channels (RGB)
    image = np.empty((FRAME_HEIGHT * FRAME_WIDTH * 3,), dtype=np.uint8)
    
    # Haar cascade is an algorithm that can detect objects in images,
    # regardless of their scale in image and location
    face = cv2.CascadeClassifier('Haarcascade/haarcascade_frontalface_default.xml')

    while True:
        # captures a frame from the camera and stores it in the image array
        camera.capture(image, 'bgr', use_video_port=True)
        # reshape the image into a 3D array
        frame = image.reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))
        # camera is mounted upsdide down so flip the image
        frame = cv2.flip(frame, 0)
        # 1.1 is the scale factor, 10 is the minimum neighbours
        faces = face.detectMultiScale(frame, 1.1, 10) 
    
        # draws rectangle on a detected face
        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # if a face is detected in the frame and the face tracking is on,
        # then call the track_face function and pass the face closest to the centre 
        if ((functions.face_tracking) and (len(faces) > 0)):
            functions.track_face( functions.find_face_closest_to_centre( faces ) )
            #print(functions.servo_steps_from_face_offset( functions.face_offset( functions.find_face_closest_to_centre( faces ) ) ) )
        
        # encodes the frame into a jpeg image
        buffer = cv2.imencode('.jpg',frame)[1]
        # converts the image into a byte array 
        # yield is used to return a value and then continue the function (sequential)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n') 

# if the file is run directly then run the app
if __name__ == '__main__': 
    # initialise the turret camera
    print("Initialising turret camera...")
    try: camera 
    except NameError: camera = None
    if camera is None:
        # camera is not initialised so initialise it
        camera = PiCamera()
        camera.resolution = (FRAME_WIDTH, FRAME_HEIGHT)
        camera.framerate = 30
        camera.iso = 1600
        camera.start_preview()
    
    app.run(debug=False, host='0.0.0.0', port=8000)
