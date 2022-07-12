from fileinput import filename
import pandas as pd
import os
import pathlib

root_dir='/workspace/L2'
directories=["/data1/", "/data2/", "/data3/"]
final_dataframe = pd.DataFrame(columns=['col1','col2', 'col3'])

for directory in directories:
    filenames = os.listdir(os.getcwd()+directory)
    for each_filename in filenames:
        file_extension = pathlib.Path(each_filename).suffix
        print("File Extension: ", file_extension)
        path = f"file://{os.getcwd()+directory+each_filename}"
        print(f"path = {path}")
        if file_extension == ".csv":
            currentdf = pd.read_csv(path)
        elif file_extension == ".json":
            currentdf = pd.read_json(path)
        # final_dataframe = pd.concat([final_dataframe, currentdf]).reset_index(drop=True)
        final_dataframe = pd.concat([final_dataframe, currentdf])
        # final_dataframe = final_dataframe.append(currentdf)

result = final_dataframe.drop_duplicates()
result.to_csv('result.csv', index=False)