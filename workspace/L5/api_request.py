import subprocess
from subprocess import DEVNULL, STDOUT, check_call
import requests

#### Command-line solution####
response1=subprocess.run(['curl', '127.0.0.1:8000/prediction'],capture_output=True).stdout

print(response1)

#### Request module solution####
response4=requests.get('http://127.0.0.1:8000/prediction').content

print(response4)
