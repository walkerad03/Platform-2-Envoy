from flask import Flask, render_template, request, send_file
import zipfile
import os

from converter import convert_to_envoy

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'File not uploaded'

    files = request.files.getlist('file')

    results = []

    for file in files:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        output_filename = f"{file.filename.removesuffix('.xlsx')}.csv"
        output_path = os.path.join('processed', output_filename)
        result = convert_to_envoy(file_path, output_path)

        os.remove(file_path)

        results.append(result)

    return render_template('upload.html', csv_files=results)


@app.route('/download/<path:file_path>')
def download(file_path):
    return send_file(file_path, as_attachment=True)


@app.route('/download/all')
def download_all_csv():
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
