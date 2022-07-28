# Dynamic Risk Assessment

## Environment

- MacBook Pro (Intel x86_64)
- MacOS Monterey 12.4
- Python version 3.8.13 installed using [mini-conda](https://github.com/conda-forge/miniforge)

### Relevant Files and Directories

```
├── reset-and-run.py     Cleans the environment and runs everything
├── apicalls.py          API client testing
├── app.py               The API server
├── config.json          Global configuration
├── deployment.py        Model deployment
├── diagnostics.py       Diags
├── fullprocess.py       Run all the scripts
├── ingesteddata
│   └── finaldata.csv    Results of data ingestion
├── ingestedfiles.txt    Record keeping of data ingestion
├── ingestion.py         Data ingestion script
├── practicedata         Development data
│   ├── dataset1.csv
│   └── dataset2.csv     Test data
├── reporting.py
├── requirements.txt     Python dependencies
├── scoring.py           Model performance
├── sourcedata
│   ├── dataset3.csv
│   └── dataset4.csv     Production data
├── testdata
│   └── testdata.csv
├── training.py          Model training
```

### How to run the code


Configure the python enviroment. You need a native python 3.8
support from your OS or use Conda to install one.

The pip method.

Check python
```
python --version
```
```
Python 3.8.12
```

Build the4 environment.
```
python -m venv venv
source activate venv/bin/activate
pip install flask pandas sklearn matplotlib requests
```

Run the API server.
```
python app.py
```

Run the main shell script.
```
bash ./reset-and-run.sh
```
