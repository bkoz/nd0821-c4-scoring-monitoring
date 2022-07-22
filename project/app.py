from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
# import create_prediction_model
# import diagnosis 
# import predict_exited_from_saved_model
from scoring import score_model
from diagnostics import dataframe_summary
from diagnostics import missing_data
from diagnostics import execution_time
from diagnostics import outdated_packages_list
from diagnostics import model_predictions
import json
import os
import logging

logging.basicConfig(level=logging.INFO)

######################Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path'])

prediction_model = None


#######################Prediction Endpoint
@app.route("/prediction", methods=['POST','OPTIONS'])
def predict():
    """
    How to test with curl:

    curl -X POST\
        --header "Content-Type: application/json"\
        localhost:8000/prediction\
        -d '{"filename" : "/testdata/testdata.csv"}'

    """
    # call the prediction function you created in Step 3
    logging.info("=> /prediction")

    #
    # Get the filename from the request body.
    #
    user_data = request.get_json()
    logging.debug(f"user_data = {user_data}")
    dataset_filename = os.getcwd() + user_data['filename']
    logging.debug(f"dataset_filename = {dataset_filename}")
    dataset = pd.read_csv(dataset_filename)

    #
    # Make and return the prediction.
    #
    y_predict = model_predictions(dataset)
    y_dictionary = {}
    y_dictionary['y_predict'] = y_predict.tolist()
    logging.info(f"y_dictionary = {y_dictionary}")

    return json.dumps(y_dictionary)

# Scoring Endpoint
@app.route("/scoring", methods=['GET','OPTIONS'])
def scoring() -> dict:
    """
    #check the score of the deployed model
    add return value (a single F1 score number)
    """
    # check the score of the deployed model
    # add return value (a single F1 score number)
    return score_model()

# Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET','OPTIONS'])
def summary() -> list:
    """
    Check means, medians, and modes for each column
    Return a list of all calculated summary statistics
    """  
    # os.getcwd() + 
    dataset_filename = "./" + dataset_csv_path + "/finaldata.csv"
    logging.info(f"summarystats: dataset_filename = {dataset_filename}")
    data_frame = pd.read_csv(dataset_filename)
    logging.info(f"summarystats: data_frame = {data_frame.info()}")
    return {"stats" : dataframe_summary(data_frame)}
#######################Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET','OPTIONS'])
def diags():        
    #check timing and percent NA values
    logging.info("=> /diagnostics")
    dataset_filename = os.getcwd() + "/" + test_data_path + "/testdata.csv"
    logging.debug(f"dataset_filename = {dataset_filename}")
    dataset = pd.read_csv(dataset_filename)
    logging.info("=> Dataframe summary")
    dataset_filename = os.getcwd() + "/"\
        + dataset_csv_path + "/finaldata.csv"
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
    package_info = outdated_packages_list().to_json()
    logging.info(package_info)
    logging.info(type(package_info))
    #add return value for all diagnostics
    return {
            "summary": summary, "percent_nas": percent_nas,
            "elapsed_times": elapsed_times,
            "package_info": package_info
            }

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
