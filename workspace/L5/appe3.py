
from flask import Flask, request
import pandas as pd

app = Flask(__name__)

def readpandas(filename):
    thedata=pd.read_csv(filename)
    return thedata

@app.route('/')
def index():
    user = request.args.get('user')
    return "Hello " + user + '\n'

@app.route('/size')
def size():
    """
    http://127.0.0.1:8000/size?filename=testdata.csv
    """
    filename = request.args.get('filename')
    thedata=readpandas(filename)
    return str(len(thedata.index))

@app.route('/summary')
def summary():
    """
    http://127.0.0.1:8000/summary?filename=testdata.csv
    """
    filename = request.args.get('filename')
    thedata=readpandas(filename)
    return str(thedata.mean(axis=0))

app.run(host='0.0.0.0', port=8000)

