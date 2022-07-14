import ast
import pandas as pd
import numpy as np

recent_r2=0.6
recent_sse=52938


#record a score in a DataFrame
previous_scores = pd.read_csv('previousscores.csv')


#find the maximum version number
max_version=previous_scores['version'].max()
print(f"max_version = {max_version}")
this_version=max_version+1
print(f"this_version = {this_version}")

#generate rows
new_row_r2 = {'metric':'r2', 'version':this_version, 'score':recent_r2}
new_row_sse = {'metric':'sse', 'version':this_version, 'score':recent_sse}

# Only update versions with better scores
if recent_sse < previous_scores.loc[previous_scores['metric']=='sse','score'].max():
    previous_scores = previous_scores.append(new_row_r2, ignore_index=True)
    previous_scores = previous_scores.append(new_row_sse, ignore_index=True)
    print("Appended new scores")

#write the dataset to a csv
previous_scores.to_csv('newscores.csv')


