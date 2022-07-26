import requests
import logging

logging.basicConfig(level=logging.INFO)

# Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:8000/"

# Call each API endpoint and store the responses
# status_code = requests.get(URL).status_code
response1 = requests.get(URL)\
    .content.decode('utf8')\
    .replace("'", '"').strip('/n')
logging.info(f"apicalls: GET / {response1}")
response2 = requests.get(URL + "scoring")\
    .content.decode('utf8')\
    .replace("'", '"').strip('/n')
response3 = requests.get(URL + "summarystats")\
    .content.decode('utf8')\
    .replace("'", '"').strip('/n')
response4 = requests.get(URL + "diagnostics")\
                         .content.decode('utf8')\
                         .replace("'", '"')\
                         .strip('/n')
data = {'filename': '/testdata/testdata.csv'}
headers = {'Content-Type': 'application/json'}
logging.debug(f"URL = {URL + 'prediction'}")
logging.debug(f"data = {data}")
logging.debug(f"headers = {headers}")
response5 = requests.post(
                          URL + "prediction",
                          json=data,
                          headers=headers
                          )\
                          .content.decode('utf8')\
                          .replace("'", '"').strip('/n')

# combine all API responses
responses = []
responses.append(response1)
responses.append(response2)
responses.append(response3)
responses.append(response4)
responses.append(response5)
logging.info(f"apicalls: GET / {responses}")

# write the responses to your workspace
for r in responses:
    print(r)

# Save the responses to a file.
response_file = "apireturns.txt"
try:
    file_handle = open(response_file, 'w')
    for response in responses:
        file_handle.write(response)
    file_handle.close()
except FileNotFoundError:
    logging.error(f"Error creating score file: {response_file}")
