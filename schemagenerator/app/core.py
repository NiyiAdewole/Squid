import pandas as pd
import logging
from typing import Dict, List, Optional
# from os import path, walk

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
    # Check the data types for each column
    data_types = [str(df[col].dtype) for col in df.columns]
    logger.warning('Columns are %s \n', column_list)
    shcema_info = {
        'columns': column_list,
        'data_types': data_types
    }

    for _, row in df.iterrows():
        record = {}
        for col in columns:
            field_name = column_mapping.get(col, col) if column_mapping else col
            record[field_name] = str(row[col]) if pd.notna(row[col]) else ""
        records.append(record)

    data = {
        'schema':shcema_info,
        'records':records,
        'info':info
    }
    
    return data

def process_excel_to_schema(file: str, column_mapping: Optional[Dict[str, str]] = None) -> str:
    # Check the file extension from the filename attribute
    if hasattr(file, 'filename'):
        filename = file.filename
    else:
        logger.error('File object does not have a filename attribute.')
        raise ValueError("Invalid file object.")
    
    logger.warning('Running process_excel_to_schema for  %s', filename)
    if filename.endswith('.csv'):
        df = pd.read_csv(file)
    elif filename.endswith(('.xlsx','.xls')):
        df = read_excel(file)
    else:
        logger.error('Unsupported file type: %s', filename)
        raise ValueError("Unsupported file type. Please upload a .csv or .xlsx/.xls file.")
    data = generate_schema(df, column_mapping)
    logger.warning('\n Schema generation returned')
    return data