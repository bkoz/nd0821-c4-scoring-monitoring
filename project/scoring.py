# from flask import Flask, session, jsonify, request
import pandas as pd
# import numpy as np
import pickle
import os
from nbformat import read
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json
import logging

logging.basicConfig(level=logging.DEBUG)

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
test_data_path = os.path.join(config['test_data_path'])
output_model_path = os.path.join(config['output_model_path'])


# Function for model scoring
def score_model():
    # this function should take a trained model, load test data
    # and calculate an F1 score for the model relative to
    # the test data it should write the result to the
    # latestscore.txt file
    
    # Read in the test data
    try:
        test_data_file = os.getcwd() + "/" + test_data_path + "/testdata.csv"
        logging.info(f"Loaded model from {test_data_file}")
        test_dataframe = pd.read_csv(test_data_file)
        X = test_dataframe.loc[:,['lastmonth_activity', 'lastyear_activity', 'number_of_employees']].values.reshape(-1, 3)
        y = test_dataframe['exited'].values
    except FileNotFoundError:
        logging.error(f"Error loading model file {test_data_file}")
        return

    # Read in the model
    output_model_dir = os.getcwd() + "/" + output_model_path
    model_filename = output_model_dir + "/trainedmodel.pkl"

    try:
        file_handle = open(model_filename, 'rb')
        model = pickle.load(file_handle)
        file_handle.close()
    except FileNotFoundError:
        logging.error(f"Error loading model file {model_filename}")
        return
    
    # Score the model.
    logging.info(f"Loaded model from {model_filename}")
    logging.info("Scoring model.")
    logging.info(f"predict = {model.predict(X)}")
    score = model.score(X, y)
    logging.info(f"score = {score}")
    score_file = output_model_dir + "/latestscore.txt"
    try:
        file_handle = open(score_file, 'w')
        file_handle.write(str(score))
        file_handle.close()
    except FileNotFoundError:
        logging.error(f"Error creating score file: {score_file}")
        return

    logging.info(f"Saving model score to {score_file}")
    

if __name__ == "__main__":
    score_model()