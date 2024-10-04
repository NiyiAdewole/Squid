import click
import json
from .core import process_excel_to_schema

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='schema.json', help='Output file name')
@click.option('--mapping', '-m', type=click.Path(exists=True), help='JSON file with column mapping')
def main(input_file, output, mapping):
    """Generate a schema from an Excel file."""
    column_mapping = None
    if mapping:
        with open(mapping, 'r') as f:
            column_mapping = json.load(f)
    
    json_schema = process_excel_to_schema(input_file, column_mapping)
    
    with open(output, 'w') as f:
        f.write(json_schema)
    
    click.echo(f"Schema generated and saved to {output}")

if __name__ == '__main__':
    main()