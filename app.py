from flask import Flask, render_template, request, send_file
import os

from main import convert_to_envoy

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'File not uploaded'

    file = request.files['file']

    if file.filename == '':
        return 'No file selected'

    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    output_path = os.path.join('processed', file.filename)
    convert_to_envoy(file_path, output_path)

    os.remove(file_path)

    return f'<a href="/download/{output_path}">Download Output File</a>'


@app.route('/download/<path:file_path>')
def download(file_path):
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('processed', exist_ok=True)
    app.run(debug=True)
