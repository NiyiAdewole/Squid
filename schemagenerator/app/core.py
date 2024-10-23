import pandas as pd
from typing import Dict, List, Optional
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def read_excel(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)

def describe_data(df: pd.DataFrame):
    # Display details
    # analysis = schema

    #  Perform analysis on the schema (Might need to make this a data frame)
    # description = {
    #     'num_fields': len(schema),
    #     'data_types': list(set(type(value).__name__ for value in schema.values())),
    #     # Add more analysis as needed
    # }
    description = {}
    return description

def generate_schema(df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
    records = []
    desc = df.describe(include='all')
    info = desc.to_dict()
    columns = df.columns
    # column_list = columns.to_dict()
    logger.warning('Running generate_schema for schema of %s \n', df)
    column_list = df.columns.to_list()
    logger.warning('Columns are %s \n', column_list)

    for _, row in df.iterrows():
        record = {}
        for col in columns:
            field_name = column_mapping.get(col, col) if column_mapping else col
            record[field_name] = str(row[col]) if pd.notna(row[col]) else ""
        records.append(record)

    data = {
        'columns':column_list, 
        'records':records,
        'info':info
    }
    
    return data

def process_excel_to_schema(file_path: str, column_mapping: Optional[Dict[str, str]] = None) -> str:
    logger.warning('Running process_excel_to_schema for  %s', file_path)
    df = read_excel(file_path)    
    data = generate_schema(df, column_mapping)
    logger.warning('\n Schema generation returned')
    return data