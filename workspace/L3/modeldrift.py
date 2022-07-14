import ast
import numpy as np
import pandas as pd
import pickle
from sklearn.metrics import mean_squared_error
import logging

logging.basicConfig(level=logging.INFO)

newr2=0.3625

with open('previousscores.txt', 'r') as f:
    f1list = ast.literal_eval(f.read())

# Raw comparision
firsttest = newr2<np.min(f1list)
print(f"newr2 = {newr2}")
print(f"min = {np.min(f1list)}")
print(firsttest)

# parametric significance test 
secondtest = newr2<np.mean(f1list)-2*np.std(f1list)
print(f"stddev = {np.std(f1list)}")
print(secondtest)

# non-parametric outlier test
iqr = np.quantile(f1list,0.75)-np.quantile(f1list,0.25)
thirdtest = newr2<np.quantile(f1list,0.25)-iqr*1.5
print(f"iqr = {iqr}")
print(thirdtest)

# Read the model using a method from the pickle module.
try:
    file_handle = open('l3final.pkl', 'rb')
    model = pickle.load(file_handle)
    file_handle.close()
except FileNotFoundError:
    logging.error(f"Error loading model file l3final.pkl")

# Read test data from a file called testdatafinal.csv, in the /L3/ directory of your workspace.
testdata = pd.read_csv('testdatafinal.csv')
X = testdata[['timeperiod']].values.reshape(-1,1)
y = testdata['sales'].values.reshape(-1,1)

# Use the model to make predictions on the test data.
y_predict = model.predict(X)
logging.info(f"y_predict = {y_predict}")
# Find the mean squared error of the model on the test data.
mse = mean_squared_error(y, y_predict)
logging.info(f"mse = {mse}")

# Read a set of the previous sum of squared error scores, found in the file l3finalscores.txt. 
# (Remember: you need to use the ast module to make sure Python reads this as a list instead of a string.)
with open('l3finalscores.txt', 'r') as f:
    sse = ast.literal_eval(f.read())

# Perform the non-parametric outlier test to determine whether the new sum of squared error 
# is high enough to indicate model drift.
iqr = np.quantile(sse, 0.75) - np.quantile(sse, 0.25)
drift = mse > np.quantile(sse, 0.25) - iqr * 1.5
print(f"iqr = {iqr}")
print(f"drift = {drift}")
