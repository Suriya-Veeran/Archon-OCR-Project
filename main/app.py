import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from ocr_processor import process_input_folder

app = Flask(__name__)
CORS(app)


@app.route('/process', methods=['POST'])
def process_input_with_model():
    data = request.json
    folder_path = data.get('folder_path')
    json_data = data.get('json_data')

    if not folder_path or not os.path.isdir(folder_path):
        return jsonify({"error": "Invalid image path"}), 400
    try:
        image_folder = data['folder_path']
        results = process_input_folder(folder_path, image_folder, json_data)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
