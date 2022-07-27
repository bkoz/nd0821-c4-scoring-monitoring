import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import json
import os
from diagnostics import model_predictions
import logging

logging.basicConfig(level=logging.INFO)

# Load config.json and get path variables
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
output_model_path = os.path.join(config['output_model_path'])
logging.info(f"output_model_path = {output_model_path}")


# Function for reporting
def score_model():
    """
    Calculate a confusion matrix using the test data and the deployed model
    Write the confusion matrix to the workspace directory.
    """
    logging.info("=> score_model")
    dataset_filename = os.getcwd() + "/" + test_data_path + "/testdata.csv"
    logging.debug(f"score_model: dataset_filename = {dataset_filename}")
    dataset = pd.read_csv(dataset_filename)
    y_predict = model_predictions(dataset)
    logging.info(f"score_model: y_predict = {y_predict}")

    y_labels = dataset.loc[:, 'exited'].values.reshape(-1, 1)
    logging.info(f"score_model: y_labels = {y_labels}")

    c_matrix = confusion_matrix(y_labels, y_predict, labels=[0, 1])
    logging.info(f"score_model: c_matrix = {c_matrix}")

    disp = ConfusionMatrixDisplay(confusion_matrix=c_matrix,
                                  display_labels=[0, 1])
    disp.plot()
    plt.title("Risk Assessment Confusion Matrix")
    #
    # create the output_model_path if necessary
    #
    try:
        os.mkdir(os.getcwd() + "/" + output_model_path)
    except FileExistsError:
        logging.info(f'{os.getcwd() + "/" + output_model_path} \
        directory exists, skipping mkdir()')

    cmatrix_filename = os.getcwd() + "/" +\
        output_model_path + "/confusionmatrix.png"
    disp.figure_.savefig(cmatrix_filename)


if __name__ == '__main__':
    score_model()
