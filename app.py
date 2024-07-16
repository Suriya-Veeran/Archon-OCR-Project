from flask import Flask, request, jsonify
from flask_cors import CORS

from persistance.entity_setup import create_tables
from service.service import process_files_with_model, save_model_details, all_models

app = Flask(__name__)

CORS(app)
create_tables()


@app.route('/add_model', methods=['POST'])
def add_model():
    data = request.get_json()
    save_model_details(data)
    return jsonify({"message": "Model and associated columns added successfully!"}), 201


@app.route('/model', methods=['POST'])
def process_input_with_model():
    data = request.get_json()
    model_id = data.get('model_id')
    input_folder_path = data.get('input_folder_path')
    response = process_files_with_model(model_id, input_folder_path)
    return jsonify(response)


@app.route('/get_models', methods=['GET'])
def get_all_models():
    return jsonify(all_models())


if __name__ == '__main__':
    app.run(debug=True)
