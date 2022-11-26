from flask import Flask, render_template, request, redirect
from functions import *

app = Flask(__name__)

#home page for turret cam
@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/data/', methods = ['GET'])
def data():
    if request.method == 'GET':
        #The URL /data/ is accessed directly so redirect to root.
        return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)