import logging
import json
from flask import Blueprint, render_template, request, session, jsonify, send_file
from .core import process_excel_to_schema
import json
import io

web = Blueprint('web', __name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@web.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@web.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.warning('No file part in the request')
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        logger.warning('No selected file')
        return 'No selected file', 400
    if file and file.filename.endswith(('.xlsx', '.xls')):
        # Process the file and generate the schema
        logger.info(f'Processing file: {file.filename}')
        schema =  process_excel_to_schema(file)
        logger.debug(f'Generate schema: {schema}')
        # Store file name and schema in session for later use
        session['filename'] =  file.filename
        session['schema'] = json.dumps(schema)
        logger.info('Schema stored in session')
        return render_template('index.html', schema=schema)
        # _, temp_path = tempfile.mkstemp(suffix='.xlsx')
        # file.save(temp_path)

@web.route('/download', methods=['POST'])
def download_schema():
    try:
        schema = session.get('schema')
        if not schema:
            return 'No schema available'
        schema_json = json.dumps(schema, indent=2)
        # Create a file-like object in memory
        buffer = io.BytesIO(schema_json.encode())
        buffer.seek(0)
        return send_file(
            buffer,
            mimetype='application/json',
            as_attachment=True,
            download_name='schema.json'
        )
    except Exception as e:
        print(f"Error analyzing schema: {e}")
        return "Internal Server Error", 500

@web.route('/analyze', methods=['POST'])
def analyze_schema():
    try:
        schema_json = session.get('schema')
        logger.debug(f'Retrieved schema from session: {schema_json}')
        if not schema_json:
            logger.warning('No schema available in session')
            return 'No schema available'
        
        # Try to parse the JSON string
        try:
            schema = json.loads(schema_json)
            logger.info('Successfully parsed schema JSON')
        except json.JSONDecodeError:
            logger.error(f'Failed to parse schema JSON: {e}')
            return "Invalid schema format in session", 400
        
        # Display details
        analysis = schema

        #  Perform analysis on the schema (Might need to make this a data frame)
        # analysis = {
        #     'num_fields': len(schema),
        #     'data_types': list(set(type(value).__name__ for value in schema.values())),
        #     # Add more analysis as needed
        # }
        logger.info(f'Completed schema analysis: {analysis}')
        return render_template('analysis.html', analysis=analysis)
    except Exception as e:
        print(f"Error analyzing schema: {e}")
        return "Internal Server Error", 500

def run_web():
    web.run(debug=True)

if __name__ == '__main__':
    run_web()