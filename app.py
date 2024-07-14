from flask import Flask, request, jsonify, send_file, render_template
import os
import glob
import uuid
import subprocess

app = Flask(__name__)

DOWNLOADS_DIR = 'downloads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    spotify_url = request.json['url']
    output_path = os.path.join(DOWNLOADS_DIR, str(uuid.uuid4()))
    os.makedirs(output_path, exist_ok=True)

    process = subprocess.Popen(
        ['spotdl', spotify_url, '--output', output_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return jsonify({"status": "error", "message": stderr.decode()}), 500

    list_of_files = glob.glob(f'{output_path}/*.mp3')
    if not list_of_files:
        return jsonify({"status": "error", "message": "Download failed"}), 500

    latest_file = max(list_of_files, key=os.path.getctime)
    relative_file_path = latest_file.replace(os.getcwd() + '/', '')

    return jsonify({"status": "success", "file_path": relative_file_path})

@app.route('/download-file/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
