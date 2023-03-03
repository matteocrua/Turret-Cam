from flask import Flask, render_template, request, redirect, Response
from functions import *
import os
# os.environ makes the webcam initialse faster
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0" 
import cv2

app = Flask(__name__)
FRAME_WIDTH = 640
FRAME_HEIGHT = 360
# new variable called camera used to capture the video of 
# the connected camera, 0 is default camera
camera = cv2.VideoCapture(0) 
# capping the resolution to reduce lag from high data transmission
camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH) 
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

# checks if camera is available
if not camera.isOpened():
    print("Cannot open camera")
    exit()

# home page for turret cam
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/data/', methods = ['GET'])
# def data():
#     if request.method == 'GET':
#         # The URL /data/ is accessed directly so redirect to root.
#         return redirect("/")

@app.route('/controls', methods = ['POST', 'GET'])
def controls():
    if request.method == 'POST': 
        form_data = request.form
        parse_user_input(form_data['control'])
        return "Success", 201
    else:
        # prevent access to /data => redirect to root
        return redirect("/")

@app.route('/speed', methods = ['POST', 'GET'])
def speed_mult():
    if request.method == 'POST':
        form_data = request.form
        print(form_data['speed'])
        return "Success", 201
    else:
        # The URL /data/ is accessed directly so redirect to root.
        return redirect("/")

@app.route('/video')
def video():
    # /video endpoint
    # provides a webcam video feed that can be used in a source for an <img> tag

    # prevent direct access to /video by checking that the referrer is the host 
    if request.headers.get("Referer") == request.host_url:
        # generate video feed, mimetype tells the browser what data to expect
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        # referer unknown => redirect to root
        return redirect("/")

def generate_frames():
    # infinite loop to continuously stream jpeg frames 
    while True:
        # success is a boolean parameter, if it is true it can read images from the camera
        success,frame = camera.read()
        if not success:
            break
        else:
            # Haar cascade is an algorithm that can detect objects in images,
            # regardless of their scale in image and location
            body = cv2.CascadeClassifier('Haarcascade\haarcascade_fullbody.xml')
            face = cv2.CascadeClassifier('Haarcascade\haarcascade_frontalface_default.xml')
            # 1.1 is the scale factor, 7 is the minimum neighbours
            bodies = body.detectMultiScale(frame, 1.1, 7) 
            # 1.1 is the scale factor, 10 is the minimum neighbours
            faces = face.detectMultiScale(frame, 1.1, 10) 

            # draws rectangle on a detected body
            for(x, y, w, h) in bodies:
                #cv2.rectangle(image, start point, end point, colour, thickness in px)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
            # draws rectangle on a detected face
            for(x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # if a face is detected in the frame then print the servo steps to the console 
            if len(faces) > 0: 
                print( servo_steps_from_face_offset( face_offset( find_face_closest_to_centre( faces ) ) ) ) 
            
            # encodes the frame into a jpeg image
            buffer = cv2.imencode('.jpg',frame)[1]
        # converts the image into a byte array 
        # yield is used to return a value and then continue the function (sequential)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n') 

# if the file is run directly then run the app
if __name__ == '__main__': 
    app.run(debug=False, host='0.0.0.0', port=80)
