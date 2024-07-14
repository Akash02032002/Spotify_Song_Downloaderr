from flask import Flask, request, jsonify, send_file, render_template
import os
import glob
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    spotify_url = request.json['url']
    output_path = 'downloads'
    os.makedirs(output_path, exist_ok=True)

    # Generate a unique file name to avoid conflicts
    unique_id = str(uuid.uuid4())
    unique_output_path = os.path.join(output_path, unique_id)
    os.makedirs(unique_output_path, exist_ok=True)

    os.system(f'spotdl {spotify_url} --output {unique_output_path}')

    # Find the downloaded file
    list_of_files = glob.glob(f'{unique_output_path}/*.mp3')
    if not list_of_files:
        return jsonify({"status": "error", "message": "Download failed"}), 500

    latest_file = max(list_of_files, key=os.path.getctime)
    relative_file_path = latest_file.replace(os.getcwd() + '/', '')
    # Create a relative file path for the frontend

    return jsonify({"status": "success", "file_path": relative_file_path})


@app.route('/download-file/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
