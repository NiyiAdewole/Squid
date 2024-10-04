from flask import Flask, render_template, request, send_file
from .core import process_excel_to_schema
import tempfile
import os
import json

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            _, temp_path = tempfile.mkstemp(suffix='.xlsx')
            file.save(temp_path)
            
            column_mapping = None
            if 'mapping' in request.files:
                mapping_file = request.files['mapping']
                if mapping_file.filename != '':
                    mapping_content = mapping_file.read().decode('utf-8')
                    column_mapping = json.loads(mapping_content)
            
            json_schema = process_excel_to_schema(temp_path, column_mapping)
            os.remove(temp_path)
            
            output_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
            output_file.write(json_schema)
            output_file.close()
            
            return send_file(output_file.name, as_attachment=True, download_name='schema.json')
    return render_template('index.html')

def run_web():
    app.run(debug=True)

if __name__ == '__main__':
    run_web()