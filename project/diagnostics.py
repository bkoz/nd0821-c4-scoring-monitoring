
import pandas as pd
# import numpy as np
# import timeit
import os
import pickle
import json
import logging

logging.basicConfig(level=logging.DEBUG)

# Load config.json and get environment variables
with open('config.json', 'r') as f:
    config = json.load(f)

logging.info("=> Configuration")
dataset_csv_path = os.path.join(config['output_folder_path'])
logging.info(f"dataset_csv_path = {dataset_csv_path}")
test_data_path = os.path.join(config['test_data_path'])
logging.info(f"test_data_path = {test_data_path}")
prod_deployment_path = os.path.join(config['prod_deployment_path'])
logging.info(f"prod_deployment_path = {prod_deployment_path}")
output_folder_path = os.path.join(config['output_folder_path'])
logging.info(f"output_folder_path = {output_folder_path}")


def model_predictions(data_frame: pd.DataFrame) -> list:
    """
    Reads a pickled model file and predicts using the given data_frame.

    It should read the deployed model from
    the directory specified in the prod_deployment_path entry of your
    config.json file.

    Args:
         data_frame - A pandas data frame.

    Returns:
         y_predict - A list of predicted values.
    """
    # Read the deployed model
    model_filename = os.getcwd() + "/"
    + prod_deployment_path + "/trainedmodel.pkl"
    logging.debug(f"model_filename = {model_filename}")

    try:
        file_handle = open(model_filename, 'rb')
        model = pickle.load(file_handle)
        file_handle.close()
        logging.info(f"Loaded {model_filename}")
    except FileNotFoundError:
        logging.error(f"Error loading model file {model_filename}")

    # Prepare the test dataset.
    columns = [
               'lastmonth_activity',
               'lastyear_activity',
               'number_of_employees']

    X = data_frame.loc[:, columns].values.reshape(-1, 3)

    # Return the calculated predictions.
    return model.predict(X)


def dataframe_summary(data_frame: pd.DataFrame) -> list:
    """
    Gather a statistical summary using the given data_frame.

    Args:
         data_frame - A pandas data frame.

    Returns:
         summary - A list representing a statistical summary.
    """
    summary = []
    columns = [
               'lastmonth_activity',
               'lastyear_activity',
               'number_of_employees']

    for column in columns:
        summary.append(data_frame[column].mean())
        summary.append(data_frame[column].median())
        summary.append(data_frame[column].std())
    return summary


# Function to get timings
def execution_time():
    # calculate timing of training.py and ingestion.py
    # return a list of 2 timing values in seconds
    return


# Function to check dependencies
def outdated_packages_list():
    # get a list of
    pass


if __name__ == '__main__':
    logging.info("=> model predictions")
    dataset_filename = os.getcwd() + "/" + test_data_path + "/testdata.csv"
    logging.debug(f"dataset_filename = {dataset_filename}")
    dataset = pd.read_csv(dataset_filename)

    y_predict = model_predictions(dataset)
    logging.info(f"y_predict = {y_predict}")

    logging.info("=> Dataframe summary")
    dataset_filename = os.getcwd() + "/"
    + output_folder_path + "/finaldata.csv"
    logging.debug(f"dataset_filename = {dataset_filename}")
    dataset = pd.read_csv(dataset_filename)
    summary = dataframe_summary(dataset)
    logging.info(f"summary = {summary}")

    logging.info("=> Execution time")
    execution_time()

    logging.info("=> Outdated packages list")
    outdated_packages_list()
