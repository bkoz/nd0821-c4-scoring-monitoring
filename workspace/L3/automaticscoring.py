#
# /L3/samplemodel.pkl. This is a pickle file that contains a trained ML model.
#  In this case, it's a logistic regression model, so the predictions it makes will be either 0's or 1's.
# /L3/testdata.csv. This is a csv file that contains a dataset you can use for testing.
#

import pandas as pd
import pickle
from sklearn import metrics
from sklearn.metrics import f1_score
import logging

logging.basicConfig(level=logging.INFO)

testdata = pd.read_csv('testdata.csv')
X = testdata[['col1','col2']].values.reshape(-1,2)
y = testdata['col3'].values.reshape(-1,1)

try:
    file_handle = open('samplemodel.pkl', 'rb')
    model = pickle.load(file_handle)
    file_handle.close()
except FileNotFoundError:
    logging.error(f"Error loading model file 'samplemodel.pkl'")

predicted=model.predict(X)

f1score=metrics.f1_score(predicted,y)
logging.info(f"Model score = {f1score}")
