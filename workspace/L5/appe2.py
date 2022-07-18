
from flask import Flask, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    """
    Example: http://127.0.0.1:8000/?user=koz
    """
    user = request.args.get('user')
    return "Hello " + user + '\n'

@app.route('/size')
def get_size():
    return "XL"


@app.route('/summary')
def get_summary():
    return "Summary"


app.run(host='0.0.0.0', port=8000)




