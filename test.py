import uuid

import yaml
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from service.service import save_model_details, process_files_with_model

with open('config.yml', 'r') as file:
    config_data = yaml.safe_load(file).get('database', {})


def create_tables_data():
    with app.app_context():
        db.create_all()


app = Flask(__name__)

url = f"postgresql://{config_data.get('username', 'postgres')}:{config_data.get('password', 'postgres')}@{config_data.get('host', 'localhost')}:{config_data.get('port', 5432)}/{config_data.get('db_name', 'postgres')}"
app.config['SQLALCHEMY_DATABASE_URI'] = url

db = SQLAlchemy()
db.init_app(app)
create_tables_data()


class Model(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trained_master_image = db.Column(db.String, nullable=True)
    columns = db.Column(db.JSON, nullable=True)


class ModelSerializer(Schema):
    id = fields.Integer()
    trained_master_image = fields.String()
    columns = fields.Dict()


def fetch_all_model():
    model_json_array = []
    all_models = Model.query.all()
    for model in all_models:
        print("model ", model)
        model_data = {
            "id": model.id,
            "trained_master_image": model.trained_master_image,
            "columns": model.columns,
        }
        print(model_data)
        model_json_array.append(model_data)
    return model_json_array


@app.route('/test/add_model', methods=['POST'])
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

@app.route('/')
def index():
    return fetch_all_model()


if __name__ == '__main__':
    app.run(debug=True)
