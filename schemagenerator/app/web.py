from flask import Blueprint, render_template, request, jsonify, send_file
from .core import process_excel_to_schema
import json
import io

web = Blueprint('web', __name__)

@web.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@web.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        # Process the file and generate the schema
        schema =  process_excel_to_schema(file)
        return render_template('index.html', schema=schema)
        # _, temp_path = tempfile.mkstemp(suffix='.xlsx')
        # file.save(temp_path)

@web.route('/download', methods=['POST'])
def download_schema():
    schema = request.form['schema']
    schema_json = json.loads(schema)

    # Create a file-like object in memory
    schema_file = io.StringIO()
    json.dump(schema_json, schema_file, indent=2)
    schema_file.seek(0)

    return send_file(
        io.BytesIO(schema_file.getvalue().encode()),
        mimetype='application/json',
        as_attachment=True
        attachment_filename='schema.json'
    )

@web.route('/analyze', methods=['POST'])
def analyze_schema():
    schema = request.form['schema']
    schema_json = json.loads(schema)

    #  Perform analysis on the schema
    analysis = analyze_schema_function(schema_json)

    return render_template('analysis.html', analysis=analysis)

def analyze_schema_function(schema):
    # This is a placeholder function. Implement your schema analysis logic here.
    analysis = {
        'num_fields': len(schema),
        'data_types': list(set(field['type'] for field in schema.values())),
        # Add more analysis as needet
    }
    return analysis

#         column_mapping = None
#         if 'mapping' in request.files:
#             mapping_file = request.files['mapping']
#             if mapping_file.filename != '':
#                 mapping_content = mapping_file.read().decode('utf-8')
#                 column_mapping = json.loads(mapping_content)
        
#         json_schema = process_excel_to_schema(temp_path, column_mapping)
#         os.remove(temp_path)
        
#         output_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
#         output_file.write(json_schema)
#         output_file.close()
        
#         return send_file(output_file.name, as_attachment=True, download_name='schema.json')
#     return render_template('index.html')

# def run_web():
#     web.run(debug=True)

# if __name__ == '__main__':
#     run_web()