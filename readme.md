# SQUID: Data Exploration Made Easy
# Readme: Internal tool for extracting, loading and tranforming small scale data repos

## Setup
To install requirements run 
```python 
pip install -r requirements.txt
```
## Usage
Use 'python run.py'

To install CLI module run the following command in the root  directory of the project:
```python
    pip install -e .
```
### Usage
To run the CLI schema generator, use the following command:
schema_generator 'path_to_file'


## Current Features
- Web User inteface
- Convert Excel file to json

## Proposed Features
- Web interface
- CLI interactivity
- Read data from csv and excel source
- Create source data schema and describe using objects
- Create rudimentary transform schema allowing modification to source columns

## Web Interface
Serve a visual inteface of different features and functions to display source and destination information
- HTTP request routing
- Views
- Extraction page: select source, click extract, display schema info
