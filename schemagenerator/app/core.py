import pandas as pd
from typing import Dict, List, Optional
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def read_excel(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)

def generate_schema(df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
    records = []
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
        'records':records
    }
    
    return data

def process_excel_to_schema(file_path: str, column_mapping: Optional[Dict[str, str]] = None) -> str:
    logger.warning('Running process_excel_to_schema for  %s', file_path)
    df = read_excel(file_path)
    data = generate_schema(df, column_mapping)
    logger.warning('\n Schema generation returned:-  %s', data)
    return data