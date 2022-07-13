import pickle
from nbformat import read
import pandas as pd
from sklearn.linear_model import LogisticRegression
import os
import logging

logging.basicConfig(level=logging.INFO)

#
# Open the previously trained model.
#
deployedmodelname = "deployedmodelname.txt"
with open(deployedmodelname, 'r') as f:
    deployedname = f.read(80)
logging.info(f"Previous model filename = {deployedname}")

filename = "datalocation.txt"
with open(filename, 'r') as f:
    datalocation = f.read(80)
logging.info(f"datalocation = {datalocation}")

###################Reading Records#############
trainingdata = pd.read_csv(os.getcwd() + datalocation)
logging.info(f"trainingdata: {trainingdata}")


##################Re-training a Model#############


X=trainingdata.loc[:,['col1','col2']].values.reshape(-1, 2)
y=trainingdata['col3'].values.reshape(-1, 1)
y=trainingdata['col3'].values
logging.info(f"X = {X}")
logging.info(f"y = {y}")

logit=LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                    intercept_scaling=1, l1_ratio=None, max_iter=100,
                    multi_class='auto', n_jobs=None, penalty='l2',
                    random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                    warm_start=False)
                    
model = logit.fit(X, y)

# Save trained model.
output_model_path = os.getcwd() + "/production/" + deployedname
file_handle = open(output_model_path, 'wb')
pickle.dump(model, file_handle)
file_handle.close()
logging.info(f"Saved model as {output_model_path}")

# Test data
logging.info(f"predict = {model.predict(X)}")
logging.info(f"score = {model.score(X, y)}")


############Pushing to Production###################




if __name__ == "__main__":
    logging.info("main")



