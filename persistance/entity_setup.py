import uuid

import yaml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

with open('config.yml', 'r') as file:
    config_data = yaml.safe_load(file).get('database', {})

app = Flask(__name__)
url = f"postgresql://{config_data.get('username', 'postgres')}:{config_data.get('password', 'postgres')}@{config_data.get('host', 'localhost')}:{config_data.get('port', 5432)}/{config_data.get('db_name', 'postgres')}"
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Model(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trained_master_image = db.Column(db.String, nullable=True)
    columns = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f'<Model {self.id}>'


def create_tables():
    with app.app_context():
        db.create_all()
