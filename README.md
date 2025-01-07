This is a Python program that creates a web application using Flask and the pydicom library to handle DICOM files. It allows users to upload DICOM files and displays their properties on a webpage.

Prerequisites
Install required libraries:

bash
pip install flask pydicom
Save the following script as app.py.


#python
```python
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
```
HTML Templates
Create a folder named templates in the same directory as app.py. Inside it, create two HTML files:

index.html

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DICOM Uploader</title>
</head>
<body>
    <h1>Upload a DICOM File</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".dcm">
        <button type="submit">Upload</button>
    </form>
</body>
</html>
```

properties.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DICOM Properties</title>
</head>
<body>
    <h1>DICOM Properties</h1>
    <table border="1">
        <thead>
            <tr>
                <th>Property</th>
                <th>Value</th>
            </tr>
        </thead>
        <tbody>
            {% for key, value in properties.items() %}
            <tr>
                <td>{{ key }}</td>
                <td>{{ value }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <a href="/">Upload Another File</a>
</body>
</html>
```
How It Works
The index.html page allows the user to upload a DICOM file.
The upload_file route saves the file, processes it with pydicom, and extracts the properties.
The properties.html template displays the extracted DICOM properties in a table.
Run the Application
Start the app by running:

```
python app.py
```
Visit http://127.0.0.1:5000 in your browser to upload and view DICOM file properties.
