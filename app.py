"""
This module contains a Flask application for file upload, conversion,
and download.

The application provides the following routes:

- `'/'`: Renders the index.html template.
- `'/upload'`: Handles file upload and conversion to Envoy format.
- `'/download/<path:file_path>'`: Downloads a file specified by the
    file_path parameter.
- `'/download/all'`: Downloads multiple CSV files as a zip archive.

Author
------
Walker Davis

Date
----
June 22, 2023
"""
import os
import zipfile
from flask import Flask, render_template, request, send_file

from converter import convert_to_envoy


app = Flask(__name__)


@app.route("/")
def index():
    """
    Renders the index.html template.

    Returns:
        The rendered index.html template.
    """
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """
    Handles file upload and conversion to Envoy format.

    Returns:
        The rendered upload.html template with processed CSV files.
    """
    if 'file' not in request.files:
        return 'File not uploaded'

    files = request.files.getlist('file')

    results = []

    for file in files:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        output_filename = f"{file.filename.removesuffix('.xlsx')}.csv"

        if output_filename.startswith("CRM Export "):
            output_filename = output_filename.removeprefix('CRM Export ')
        output_path = os.path.join('processed', output_filename)
        result = convert_to_envoy(file_path, output_path)

        os.remove(file_path)

        results.append(result)

    return render_template('upload.html', csv_files=results)


@app.route('/download/<path:file_path>')
def download(file_path):
    """
    Downloads a file specified by the file_path parameter.

    Args:
        file_path (str): The path of the file to be downloaded.

    Returns:
        The downloaded file as an attachment.
    """
    return send_file(file_path, as_attachment=True)


@app.route('/download/all')
def download_all_csv():
    """
    Downloads multiple CSV files as a zip archive.

    Returns:
        The zip archive containing the specified CSV files.
    """
    filenames = request.args.getlist('filenames')
    zip_filepath = 'out.zip'

    with zipfile.ZipFile(zip_filepath, 'w') as zip_file:
        for filename in filenames:
            zip_file.write(filename)

    return send_file(zip_filepath, as_attachment=True)


if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('processed', exist_ok=True)
    app.run(port=8080)
