
import pandas as pd
import numpy as np
import timeit
import os
import json

##################Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path']) 

# Function to get model predictions
def model_predictions(dataset: pd.DataFrame) -> list:
    """
    This function should take an argument that consists of a dataset, 
    in a pandas DataFrame format. It should read the deployed model from 
    the directory specified in the prod_deployment_path entry of your 
    config.json file.

    The function uses the deployed model to make predictions for each row 
    of the input dataset. 
    
    The output should be a list of predictions. 
    This list should have the same length as the number of rows in the 
    input dataset.
    """
    # read the deployed model and a test dataset, calculate predictions
    return # return value should be a list containing all predictions

# Function to get summary statistics
def dataframe_summary():
    # calculate summary statistics here
    return # return value should be a list containing all summary statistics

# Function to get timings
def execution_time():
    # calculate timing of training.py and ingestion.py
    return # return a list of 2 timing values in seconds

# Function to check dependencies
def outdated_packages_list():
    # get a list of
    pass


if __name__ == '__main__':
    model_predictions()
    dataframe_summary()
    execution_time()
    outdated_packages_list()





    
