import logging
import json
from flask import Blueprint, render_template, request, redirect, session, send_file, url_for, flash
from .core import process_excel_to_schema, sample_tables
from .models import db, User
import json
import io

web = Blueprint('web', __name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@web.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@web.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('web.register'))

        # Create a new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('web.index'))
    return render_template('register.html')

@web.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.warning('No file part in the request')
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        logger.warning('No selected file')
        return 'No selected file', 400
    if file and file.filename.endswith(('.xlsx', '.xls', '.csv')):
        # Process the file and generate the schema
        logger.info(f'\n\n Processing file, stepping into core now : {file.filename}')
        data = process_excel_to_schema(file)
        # Store file name and data in session for later use
        # ToDo: Add a limit to how much of data is sampled for session storage
        session['filename'] =  file.filename
        session['filedata'] = data

        # Describe data schema - Get info, number of rows types for each column etc
        return render_template('index.html', data=data)

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
        logger.debug('Retrieving data from session')
        if not data:
            logger.warning('No data file loaded in session')
            return 'No data file available'
        
        # Try to parse the JSON string
        logger.info('Try to parse the JSON string')
        try:
            data_json = json.dumps(data, indent = 2, sort_keys = True)
            logger.debug("Successfully parsed schema JSON")
        except json.JSONDecodeError:
            logger.error('Failed to parse schema JSON: %s', {e})
            return "Invalid schema format in session", 400
        
        logger.info('Quick analysis complete!')
        return render_template('analysis.html', title='analyze this', analysis=data, preview=data_json)
    except Exception as e:
        print('Error analyzing schema: %s', e)
        return "Internal Server Error", 500

@web.route('/design', methods=['POST', 'GET'])
def design_schema():

    logger.info('Loading design page')
    # samples = sample_tables()
    try:
        data = session.get('filedata')
        # data = session.get('filedata')
        if not data:
            logger.info('nothing in session', session.get('filedata'))
            data = sample_tables()
        else:
            logger.info('something in session', session.get('filedata'))
            logger.info('Loaded file data', data)
            # tables = json.dumps(data, indent=2, sort_keys=True)
        return render_template('design.html', title='design this', tables=data)
    except Exception as e:
        logger.error('Problem loading session filedata', e )
        return 'No tables available', 404
    # else:
    # return render_template('index.html', data=tables)

def run_web():
    logger.info("Running web...")
    web.run(debug=True)

if __name__ == '__main__':
    run_web()