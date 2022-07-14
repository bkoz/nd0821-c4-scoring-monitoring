import os
import json
import shutil
import logging

logging.basicConfig(level=logging.INFO)

# Load config.json and correct path variable
with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
prod_deployment_path = os.path.join(config['prod_deployment_path'])
output_model_path = os.path.join(config['output_model_path'])


# function for deployment
# Does this function name make sense?
def store_model_into_pickle() -> None:
    """
    Copy the latest pickle file, the latestscore.txt value,
    and the ingestfiles.txt file into the deployment directory

    Args: None
    """

    #
    # create the dest_dir if necessary
    #
    dest_dir = os.getcwd() + "/" + prod_deployment_path

    try:
        (os.mkdir(dest_dir))
    except FileExistsError:
        logging.info(f"{dest_dir}\
                    directory exists, skipping mkdir()")

    prod_model_file = os.getcwd() + "/" + output_model_path + \
        "/trainedmodel.pkl"
    prod_score_file = os.getcwd() + "/" + output_model_path + \
        "/latestscore.txt"
    prod_injested_files = os.getcwd() + "/ingestedfiles.txt"

    logging.debug(f"{prod_model_file} {dest_dir}")
    logging.debug(f"{prod_score_file} {dest_dir}")
    logging.debug(f"{prod_injested_files} {dest_dir}")

    shutil.copy2(prod_model_file, dest_dir)
    shutil.copy2(prod_score_file, dest_dir)
    shutil.copy2(prod_injested_files, dest_dir)


if __name__ == "__main__":
    store_model_into_pickle()
