from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        #The URL /data is accessed directly so redirect to root.
        return redirect("/", code=302)
    if request.method == 'POST':
        form_data = request.form
        print(form_data['control'])
        return "Success", 201

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)

