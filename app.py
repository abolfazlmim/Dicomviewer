from flask import Flask, render_template, request, redirect, url_for
import os
import pydicom

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'dcm'}

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        dicom_data = pydicom.dcmread(filepath)
        dicom_properties = {tag: str(dicom_data[tag].value) for tag in dicom_data.dir()}
        return render_template('properties.html', properties=dicom_properties)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
