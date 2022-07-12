# Dynamic Risk Assessment

## Environment

- MacBook Pro (Intel x86_64)
- MacOS Monterey 12.4
- Python version 3.8.13 installed using [mini-conda](https://github.com/conda-forge/miniforge)

### File and Directories

```
├── apicalls.py
├── app.py
├── config.json          Global configuration
├── deployment.py
├── diagnostics.py
├── fullprocess.py
├── ingesteddata
│   └── finaldata.csv     Results of data ingestion
├── ingestedfiles.txt     Record keeping of data ingestion
├── ingestion.py          Data ingestion script
├── practicedata          Development data
│   ├── dataset1.csv
│   └── dataset2.csv
├── reporting.py
├── requirements.txt      Python dependencies
├── scoring.py
├── sourcedata
│   ├── dataset3.csv
│   └── dataset4.csv
├── testdata
│   └── testdata.csv
├── training.py
└── wsgi.py
```

### Steps

#### 1) Data Ingestion

Reads csv files and creates `ingestedfiles.txt` and `finaldata.csv`.

```
cd project
python ingestion.py
```

#### 2) Training, Scoring, and Deploying an ML Model

#### 3) Model and Data Diagnostics

#### 4) Reporting

#### 5) Process Automation

#### 6) Additional Tasks
- PDF reports
- Time Trends
- Database setup