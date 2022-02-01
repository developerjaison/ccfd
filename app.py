from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import pandas as pd
ALLOWED_EXTENSIONS = {'csv'}
app = Flask(__name__)
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
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
  # check if the post request has the file part
  if 'file' not in request.files:
    flash('No file part')
    return 'No file part'
  file = request.files['file']
  # If the user does not select a file, the browser submits an
  # empty file without a filename.
  if file.filename == '':
    flash('No selected file')
    return 'No selected file'
  if file and allowed_file(file.filename):
    df = pd.read_csv(request.files.get('file'))
    data = df.sample(frac=0.1, random_state = 1)
    Fraud = data[data['Class'] == 1]
    Valid = data[data['Class'] == 0]
    outlier_fraction = len(Fraud)/float(len(Valid))
    fraudcases = 'Fraud Cases: {}'.format(len(data[data['Class'] == 1]))
    validcases = 'Valid Transactions: {}'.format(len(data[data['Class'] == 0]))
    # result = {
    #   Fraud:Fraud,
    #   Valid:Valid
    # }
    return render_template('success.html', fraudcases=fraudcases, validcases=validcases)
  return "NULL"
if __name__ == '__main__':
   app.run()