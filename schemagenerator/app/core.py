import pandas as pd
from typing import Dict, List, Optional

def read_excel(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)

def generate_schema(df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
    schema = []
    columns = df.columns

    for _, row in df.iterrows():
        schema_item = {}
        for col in columns:
            field_name = column_mapping.get(col, col) if column_mapping else col
            schema_item[field_name] = str(row[col]) if pd.notna(row[col]) else ""
        schema.append(schema_item)
    
    return schema

def schema_to_json(schema: List[Dict[str, str]]) -> str:
    import json
    return json.dumps(schema, indent=2)

def process_excel_to_schema(file_path: str, column_mapping: Optional[Dict[str, str]] = None) -> str:
    df = read_excel(file_path)
    schema = generate_schema(df, column_mapping)
    return schema_to_json(schema)