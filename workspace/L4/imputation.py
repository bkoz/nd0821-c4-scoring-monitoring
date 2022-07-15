import ast
import pandas as pd
import os


csv_file = os.getcwd() + '/' + 'samplefile3.csv'
csv_file = os.getcwd() + '/workspace/L4/' + 'samplefile3.csv'
print(f"csv_file = {csv_file}")
thedata=pd.read_csv(csv_file)

nas=list(thedata.isna().sum())
napercents=[nas[i]/len(thedata.index) for i in range(len(nas))]


thedata['col1'].fillna(pd.to_numeric(thedata['col1'],errors='coerce').mean(skipna=True), inplace = True)
thedata['col2'].fillna(pd.to_numeric(thedata['col2'],errors='coerce').mean(skipna=True), inplace = True)
thedata['col3'].fillna(pd.to_numeric(thedata['col3'],errors='coerce').mean(skipna=True), inplace = True)

print(thedata.head())

print(f"column 1 mean = {thedata['col1'].mean(skipna=True)}")