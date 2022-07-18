from flask import Flask, request
import pandas as pd
import pickle
import logging

# logging.basicConfig(level=logging.INF0)

app = Flask(__name__)

def readpandas(filename):
    thedata=pd.read_csv(filename)
    return thedata

@app.route('/prediction')
def predict():
    """
    http://127.0.0.1:8000/summary?filename=testdata.csv
    """
    filename = 'predictiondata.csv'
    thedata=readpandas(filename)
    X = thedata[['col1', 'col2']].values.reshape(-1,2)


    try:
        model_filename = 'deployedmodel.pkl'
        file_handle = open(model_filename, 'rb')
        model = pickle.load(file_handle)
        file_handle.close()
    except FileNotFoundError:
        logging.error(f"Error loading model file {model_filename}")

    predicted=model.predict(X)
    logging.info(f"predicted = {predicted}")

    return str(f"predicted: {predicted}")

app.run(host='0.0.0.0', port=8000)
