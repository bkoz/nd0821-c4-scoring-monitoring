
import pandas as pd
# import numpy as np
# import timeit
import time
import os
import subprocess
import pickle
import json
import logging

logging.basicConfig(level=logging.INFO)

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
    model_filename = os.getcwd() + "/"\
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


def missing_data(data_frame: pd.DataFrame) -> list:
    """
    Count the number of NA values in each column of your dataset.
    Then, it needs to calculate what percent of each column
    consists of NA values.

    The function should count missing data for the dataset stored in the
    directory specified by output_folder_path in config.json.
    It will return a list with the same number of elements as the number
    of columns in your dataset. Each element of the list will be the
    percent of NA values in a particular column of your data.
    """
    nas = list(data_frame.isna().sum())
    na_percents = [nas[i] / len(data_frame.index) for i in range(len(nas))]
    return na_percents


# Function to get timings
def execution_time() -> list:
    # calculate timing of training.py and ingestion.py
    # return a list of 2 timing values in seconds
    training_t0 = time.time()
    subprocess.run(['python3', 'training.py'], capture_output=True)
    training_t1 = time.time()
    ingestion_t0 = time.time()
    subprocess.run(['python3', 'ingestion.py'], capture_output=True)
    ingestion_t1 = time.time()
    elapsed_times_list = []
    elapsed_times_list.append(training_t1 - training_t0)
    elapsed_times_list.append(ingestion_t1 - ingestion_t0)
    return elapsed_times_list


# Function to check dependencies
def outdated_packages_list():
    """
    output a table with three columns: the first column will show
    the name of a Python module that you're using; the second column
    will show the currently installed version of that Python module,
    and the third column will show the most recent available version
    of that Python module.

    This can be done with linux commands:
    Something like:
    pip list --outdated | tail +3 | awk '{print $1 " " $2 " " $3}'
    python -m pip list --outdated | cut -w -f 1-3
    """
    table = subprocess.check_output(
                                    [
                                     'python',
                                     '-m' 'pip',
                                     'list',
                                     '--outdated'
                                     ]
                                     )
    s = table.split()

    package_list = []
    for b in s:
        string = b.decode('utf-8')
        package_list.append(string)

    df = pd.DataFrame(
                      columns=[
                               package_list[0],
                               package_list[1],
                               package_list[2]
                               ]
                      )

    for i in range(8, len(package_list), 4):
        row = {'Package': package_list[i],
               'Version': package_list[i+1],
               'Latest': package_list[i+2]}
        df = df.append(row, ignore_index=True)

    return df


if __name__ == '__main__':
    logging.info("=> model predictions")
    dataset_filename = os.getcwd() + "/" + test_data_path + "/testdata.csv"
    logging.debug(f"dataset_filename = {dataset_filename}")
    dataset = pd.read_csv(dataset_filename)

    y_predict = model_predictions(dataset)
    logging.info(f"y_predict = {y_predict}")

    logging.info("=> Dataframe summary")
    dataset_filename = os.getcwd() + "/"\
        + output_folder_path + "/finaldata.csv"
    logging.debug(f"dataset_filename = {dataset_filename}")
    dataset = pd.read_csv(dataset_filename)
    summary = dataframe_summary(dataset)
    logging.info(f"summary = {summary}")
    logging.info("=> Missing Data")
    percent_nas = missing_data(dataset)
    logging.info(f"=> percent_nas = {percent_nas}")

    logging.info("=> Execution time")
    elapsed_times = execution_time()
    logging.info(f"=> training and ingestion time = {elapsed_times}")

    logging.info("=> Generated outdated packages list")
    logging.info("=> This could take a minute.")
    logging.info(outdated_packages_list())
