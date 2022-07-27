

import training
import scoring
import deployment
import diagnostics
import reporting
import pickle
from sklearn.metrics import f1_score
import pandas as pd
import os
import json
import subprocess
import logging

# Load config.json and get environment variables
with open('config.json', 'r') as f:
    config = json.load(f)

logging.info("fullprocess: => Configuration")
dataset_csv_path = os.path.join(config['output_folder_path'])
logging.info(f"fullprocess: dataset_csv_path = {dataset_csv_path}")
test_data_path = os.path.join(config['test_data_path'])
logging.info(f"fullprocess: test_data_path = {test_data_path}")
prod_deployment_path = os.path.join(config['prod_deployment_path'])
logging.info(f"fullprocess: prod_deployment_path = {prod_deployment_path}")
output_folder_path = os.path.join(config['output_folder_path'])
logging.info(f"fullprocess: output_folder_path = {output_folder_path}")
input_folder_path = os.path.join(config['input_folder_path'])
logging.info(f"fullprocess: input_folder_path = {input_folder_path}")
output_model_path = os.path.join(config['output_model_path'])
logging.info(f"fullprocess: output_model_path = {output_model_path}")

# Check if the filenames in sourcedata differ from 'ingestedfiles.txt'
# If so, call the ingestion.py script.

# Second, determine whether the source data folder has files that aren't listed in ingestedfiles.txt
# List the files in the input_folder_path directory

# Get the input_folder from the global config
files2=os.listdir(input_folder_path)
ingested_files_filename = 'ingestedfiles.txt'

try:
    file_handle=open(ingested_files_filename)
    files = file_handle.readlines()
except FileNotFoundError:
    logging.error(f"Error reading ingested_files_file:\
        {ingested_files_filename}")

# Strip out \n from each filename.
original_files = [file.strip() for file in files]
new_files = [file.strip() for file in files2]

logging.info(f'original_files = {original_files}')
logging.info(f'new_files = {new_files}')
logging.info(f'original_files == new_files = {original_files == new_files}')

# Deciding whether to proceed, part 1
# if you found new data, you should proceed. otherwise, do end the process here
if (original_files != new_files):
    logging.info("fullprocess: launching ingestion.py")
    subprocess.run(['python3', 'ingestion.py'], capture_output=True)
else:
    logging.info("fullprocess: not running ingestion.py")
    exit()


# Checking for model drift
# check whether the score from the deployed model is different from the score from the model that uses the newest ingested data

# Get the latest model score.
logging.info("fullprocess: Checking for model drift")
score_file = os.getcwd() + '/' + prod_deployment_path + '/latestscore.txt'
logging.info(f'fullprocess: latest score filename = {score_file}')

try:
    file_handle = open(score_file, 'r')
    latest_score = float(file_handle.read())
    logging.info(f'fullprocess: latest_score = {latest_score}')
    file_handle.close()
except FileNotFoundError:
    logging.info(f'fullprocess: scoring file {score_file} not found')

#
# Deciding whether to proceed, part 2
# if you found model drift, you should proceed. otherwise, do end the process here
#
# Load the latest dataset.
try:
    dataset_filename = os.getcwd() + '/' + output_folder_path + '/finaldata.csv'
    logging.info(f'fullprocess: dataset_filename = {dataset_filename}')
    data_frame = pd.read_csv(dataset_filename)
    X = data_frame.loc[:, ['lastmonth_activity', 'lastyear_activity',
                                'number_of_employees']]\
        .values.reshape(-1, 3)
    y = data_frame['exited'].values
except FileNotFoundError:
    logging.error(f"Error loading model file {dataset_filename}")

# Load the model and score it using the most recent data.
model_filename = os.getcwd() + "/" + prod_deployment_path + "/trainedmodel.pkl"

try:
    file_handle = open(model_filename, 'rb')
    model = pickle.load(file_handle)
    file_handle.close()
except FileNotFoundError:
    logging.error(f"Error loading model file {model_filename}")

# Score the model.
# Should I be just calling scoring.py?
logging.info(f"Loaded model from {model_filename}")
logging.info("Scoring model.")
predicted = model.predict(X)
logging.info(f"predict = {predicted}")
score = f1_score(predicted, y)
logging.info(f"F1 score = {score}")

# Re-deployment
# if you found evidence for model drift, re-run the deployment.py script
if (score != latest_score):
    logging.info(f'fullprocess: model drift detected!')
    logging.info(f'fullprocess: running deployment.py script')
    subprocess.run(['python3', 'deployment.py'], capture_output=True)

# Diagnostics and reporting
# run diagnostics.py and reporting.py for the re-deployed model
logging.info(f'fullprocess: running diagnostics.py script')
subprocess.run(['python3', 'diagnostics.py'], capture_output=True)
logging.info(f'fullprocess: running reporting.py script')
subprocess.run(['python3', 'reporting.py'], capture_output=True)