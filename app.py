from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/test')
def say_hello():
  return 'Hello from Server'
  
@app.route('/upload')
def upload():
  return render_template('upload.html')
  
@app.route('/success', methods=["POST"])
def success():
  return "SUCCUSS"