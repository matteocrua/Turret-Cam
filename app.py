from flask import Flask, render_template, request, redirect, Response
from picamera import PiCamera
import numpy as np
import cv2
import functions
from io import BytesIO
from Turret import *

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
        #print(form_data['speed'])
        return "Success", 201
    else:
        # The URL /data/ is accessed directly so redirect to root.
        return redirect("/")

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

def generate_frames():
    # infinite loop to continuously stream jpeg frames
    image = np.empty((FRAME_HEIGHT * FRAME_WIDTH * 3,), dtype=np.uint8)
    
    # Haar cascade is an algorithm that can detect objects in images,
    # regardless of their scale in image and location
    face = cv2.CascadeClassifier('Haarcascade/haarcascade_frontalface_default.xml')

    while True:
        # success is a boolean parameter, if it is true it can read images from the camera
        camera.capture(image, 'bgr', use_video_port=True)
        frame = image.reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))
        frame = cv2.flip(frame, 0)
        # 1.1 is the scale factor, 10 is the minimum neighbours
        faces = face.detectMultiScale(frame, 1.1, 10) 
    
        # draws rectangle on a detected face
        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # if a face is detected in the frame then print the servo steps to the console 
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
        camera = PiCamera()
        camera.resolution = (FRAME_WIDTH, FRAME_HEIGHT)
        camera.framerate = 30
        camera.iso = 1600
        camera.start_preview()
    
    app.run(debug=False, host='0.0.0.0', port=8000)
