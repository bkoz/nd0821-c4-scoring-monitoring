# from flask import Flask, session, jsonify, request
import pandas as pd
import pickle
import os
from sklearn.linear_model import LogisticRegression
import json
import logging

logging.basicConfig(level=logging.INFO)

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
model_path = os.path.join(config['output_model_path'])
logging.debug(f"dataset_csv_path: {dataset_csv_path}")
logging.debug(f"model_path: {model_path}")


# Function for training the model
def train_model():
    # Read data and create a data frame
    csv_file_path = os.getcwd() + "/" + dataset_csv_path + "/finaldata.csv"
    dataframe = pd.read_csv(csv_file_path)
    logging.debug(f"dataframe:\n {dataframe}")

    # Create the training sets.
    X = dataframe.loc[:, ['lastmonth_activity',
                          'lastyear_activity',
                          'number_of_employees']].values.reshape(-1, 3)
    y = dataframe['exited'].values
    logging.debug(f"X = {X}")
    logging.debug(f"y = {y}")

    # use this logistic regression for training
    # BK - Changed multi_class from 'warn' to 'auto'.
    logits = LogisticRegression(C=1.0, class_weight=None, dual=False,
                                fit_intercept=True,
                                intercept_scaling=1, l1_ratio=None,
                                max_iter=100,
                                multi_class='auto', n_jobs=None,
                                penalty='l2',
                                random_state=0, solver='liblinear',
                                tol=0.0001, verbose=0,
                                warm_start=False)

    # fit the logistic regression to your data
    model = logits.fit(X, y)

    logging.info(f"predict = {model.predict(X)}")
    logging.info(f"score = {model.score(X, y)}")

    # write the trained model to your workspace in a
    # file called trainedmodel.pkl
    output_model_dir = os.getcwd() + "/" + model_path
    output_model_path = output_model_dir + "/trainedmodel.pkl"
    #
    # Create the output_model_dir if it does not exist.
    #
    try:
        (os.mkdir(output_model_dir))
    except FileExistsError:
        logging.error(f"{output_model_dir}\
                     directory exists, skipping mkdir()")
    file_handle = open(output_model_path, 'wb')
    pickle.dump(model, file_handle)
    file_handle.close()
    logging.info(f"Saved model as {output_model_path}")


if __name__ == "__main__":
    train_model()
