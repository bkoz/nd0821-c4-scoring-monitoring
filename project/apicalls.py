import requests
import logging
import json
import subprocess
import os

logging.basicConfig(level=logging.DEBUG)

# Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:8000/"

# Call each API endpoint and store the responses
# status_code = requests.get(URL).status_code
# response1 = requests.get(URL).content.decode('utf8').replace("'", '"').strip('/n')
# logging.info(f"apicalls: GET / {response1}")
# response2 = requests.get(URL + "scoring").content.decode('utf8').replace("'", '"').strip('/n')
# response3 = requests.get(URL + "summarystats").content.decode('utf8').replace("'", '"').strip('/n')
#response4 = requests.get(URL + "diagnostics").content.decode('utf8').replace("'", '"').strip('/n')
data={"filename" : f'{os.getcwd()} + "/" + "/testdata/testdata.csv"'}
data={'filename' : '/testdata/testdata.csv'}
headers={'Content-Type': 'application/json'}
logging.debug(f"URL = {URL + 'prediction'}")
logging.debug(f"data = {data}")
logging.debug(f"headers = {headers}")
response5 = requests.post(URL + "prediction",
                          json=data,
                          headers=headers).content.decode('utf8').replace("'", '"').strip('/n')

# response5=subprocess.run(
#     ['curl', '127.0.0.1:8000/prediction',
#     '-d={"filename" : "/testdata/testdata.csv"}',
#     '--header "Content-Type: application/json"'],
#     capture_output=True).stdout
print(f"response5 = {response5}")

# combine all API responses
responses = []
# responses.append(response1)
# responses.append(response2)
# responses.append(response3)
#responses.append(response4)
responses.append(response5)
logging.info(f"apicalls: GET / {responses}")

# write the responses to your workspace
for r in responses:
    print(r)



