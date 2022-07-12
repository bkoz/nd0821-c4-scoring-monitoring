import pandas as pd
# import numpy as np
import os
import json
from datetime import datetime
import pathlib
import logging

# BK
logging.basicConfig(level=logging.DEBUG)

#
# Load config.json and get input and output paths
#
with open('config.json', 'r') as f:
    config = json.load(f)

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']

logging.debug(f"input_folder_path: {input_folder_path}")


def merge_multiple_dataframe() -> None:
    """
    Description: Perform data ingestion, agregation and de-duplication
    from multiple csv files and write the resulting output file.
    """

    final_dataframe = pd.DataFrame()
    filenames = os.listdir(input_folder_path)
    logging.debug(f"filenames: {filenames}")

    # Create record keeping file.
    outputlocation='ingestedfiles.txt'
    file_handle = open(outputlocation, 'w')

    for each_filename in filenames:
        file_extension = pathlib.Path(each_filename).suffix
        if file_extension == ".csv":
            file_path = f"{input_folder_path}/{each_filename}"
            logging.debug(f"Reading filename: {file_path}")
            currentdf = pd.read_csv(file_path)
            
            # Perform record keeping of each file read.
            dateTimeObj=datetime.now()
            thetimenow=str(dateTimeObj.year)+ '/'+str(dateTimeObj.month)+\
                            '/'+str(dateTimeObj.day)
            allrecords=[input_folder_path, each_filename, len(currentdf.index), thetimenow]
            logging.debug(f"Writing record keeping data for {each_filename}.")
            logging.debug(f"record = {allrecords}.")
            file_handle.write(str(allrecords))
            file_handle.write("\n")
            logging.debug(f"element type {type(allrecords)}")

            final_dataframe = pd.concat([final_dataframe, currentdf])

    result = final_dataframe.drop_duplicates()

    #
    # Create the output_folder_path if it does not exist.
    #
    try:
        (os.mkdir(output_folder_path))
    except FileExistsError:
        logging.info(f"{output_folder_path}\
                     directory exists, skipping mkdir()")

    #
    # Write the final csv file.
    #
    output_file_path = f"{output_folder_path}/finaldata.csv"
    logging.debug(f"Writing final csv file to: {output_file_path}")
    result.to_csv(output_file_path, index=False)

    #
    # Save a record of the data ingestion to a file called
    # output_file_path/ingestedfiles.txt
    #
    

if __name__ == '__main__':
    merge_multiple_dataframe()
