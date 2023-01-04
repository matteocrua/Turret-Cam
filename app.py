from flask import Flask, render_template, request, redirect, Response
from functions import *
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0" #makes the webcam initialse faster
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0) #new class called camera used to capture the video of the connected camera, 0 is default camera
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #capping the resolution to reduce lag from high data transmission
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

#checks if camera is available
if not camera.isOpened():
    print("Cannot open camera")
    exit()

#home page for turret cam
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data/', methods = ['GET'])
def data():
    if request.method == 'GET':
        #The URL /data/ is accessed directly so redirect to root.
        return redirect("/", code=302)

@app.route('/data/controls', methods = ['POST', 'GET'])
def controls():
    if request.method == 'GET':
        #The URL /data/ is accessed directly so redirect to root.
        return redirect("/", code=302)
    if request.method == 'POST': 
        form_data = request.form
        parse_user_input(form_data['control'])
        return "Success", 201

@app.route('/data/speed', methods = ['POST', 'GET'])
def speed_mult():
    if request.method == 'GET':
        #The URL /data/ is accessed directly so redirect to root.
        return redirect("/", code=302)
    if request.method == 'POST':
        form_data = request.form
        print(form_data['speed'])
        return "Success", 201

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    while True:
        success,frame = camera.read() #success is a boolean parameter, if it is true it can read images from the camera
        #success = False
        if not success:
            break
        else:
            #return False
            buffer = cv2.imencode('.jpg',frame)[1]
            frame = buffer.tobytes()
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') #use yield instead of return as yield iterates over a sequence such as the frames

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
