

import training
import scoring
import deployment
import diagnostics
import reporting
import os
import json
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

# Get this from the global config
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
    
# Second, determine whether the source data folder has files that aren't listed in ingestedfiles.txt
# List the files in the input_folder_path directory


##################Deciding whether to proceed, part 1
#if you found new data, you should proceed. otherwise, do end the process here


##################Checking for model drift
#check whether the score from the deployed model is different from the score from the model that uses the newest ingested data


##################Deciding whether to proceed, part 2
#if you found model drift, you should proceed. otherwise, do end the process here



##################Re-deployment
#if you found evidence for model drift, re-run the deployment.py script

##################Diagnostics and reporting
#run diagnostics.py and reporting.py for the re-deployed model







