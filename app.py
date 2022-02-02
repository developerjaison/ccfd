from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score, matthews_corrcoef
from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mpld3
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
    fraudAmount = Fraud.Amount
    validAmount = Valid.Amount
    corrmat = data.corr()
    fig = plt.figure(figsize = (5, 5))
    sns.heatmap(corrmat, vmax = .8, square = True)
    plot = mpld3.fig_to_html(fig)
    X = data.drop(['Class'], axis = 1)
    Y = data["Class"]
    xData = X.values
    yData = Y.values
    xTrain, xTest, yTrain, yTest = train_test_split(xData, yData, test_size = 0.2, random_state = 42)
    # random forest model creation
    rfc = RandomForestClassifier()
    rfc.fit(xTrain, yTrain)
    # predictions
    yPred = rfc.predict(xTest)
    acc = format(accuracy_score(yTest, yPred))
    prec = format(precision_score(yTest, yPred))
    rec = format(recall_score(yTest, yPred))
    f1 = format(f1_score(yTest, yPred))
    MCC = format(matthews_corrcoef(yTest, yPred))
    LABELS = ['Normal', 'Fraud']
    conf_matrix = confusion_matrix(yTest, yPred)
    fig1 = plt.figure(figsize =(5, 5))
    sns.heatmap(conf_matrix, xticklabels = LABELS,
                yticklabels = LABELS, annot = True, fmt ="d")
    plt.title("Confusion matrix")
    plt.ylabel('True class')
    plt.xlabel('Predicted class')
    plot1 = mpld3.fig_to_html(fig1)
    
    return render_template('success.html', 
    fraudcases=fraudcases, validcases=validcases, 
    outlier_fraction=outlier_fraction, fraudAmount=fraudAmount, 
    validAmount=validAmount, plot=plot, acc=acc, prec=prec,
    rec=rec, f1=f1, MCC=MCC, plot1=plot1)
  return "NULL"
if __name__ == '__main__':
   app.run()