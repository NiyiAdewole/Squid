import logging
import json
from flask import Blueprint, render_template, request, session, send_file, jsonify
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
        logger.info(f'\n\n Processing file, stepping into core now : {file.filename}')
        data = process_excel_to_schema(file)
        # data =  json.dumps(data)
        logger.debug(f'\n\n Exited core | Generate schema: {type(data)}')
        # Store file name and schema in session for later use
        session['filename'] =  file.filename
        # session['columns'] = json.dump(data.columns)
    
        session['columns'] = data['columns']
        session['filedata'] = data
        logger.info('Uploaded file stored in session')

        # Describe data schema
        # Get info, number of rows types for each column etc
        
        return render_template('index.html', data=data)
        # _, temp_path = tempfile.mkstemp(suffix='.xlsx')
        # file.save(temp_path)


@web.route('/download', methods=['POST'])
def download_schema():
    try:
        data = session.get('data')
        if not data:
            return 'No schema available'
        data_json = json.dumps(data, indent=2)
        # Create a file-like object in memory
        buffer = io.BytesIO(data_json.encode())
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

@web.route('/analyze', methods=['POST', 'GET'])
def analyze_schema():
    try:
        logger.info('Loading analysis page')
        data = session.get('filedata')
        # columns = data_json
        logger.debug(f'Retrieved schema from session: ', data)
        if not data:
            logger.warning('No schema available in session')
            return 'No schema available'
        
        # Try to parse the JSON string
        try:
            logger.info('Try to parse the JSON string')
            data_json = json.dumps(data)
            logger.info('Successfully parsed schema JSON', data_json)
        except json.JSONDecodeError:
            logger.error(f'Failed to parse schema JSON: {e}')
            return "Invalid schema format in session", 400
        
        logger.info(f'Completed schema analysis: {data}')
        return render_template('analysis.html', title='analyze this', analysis=data, data=data)
    except Exception as e:
        print(f"Error analyzing schema: {e}")
        return "Internal Server Error", 500

def run_web():
    web.run(debug=True)

if __name__ == '__main__':
    run_web()