import base64
import json

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bean.beans import ModelBean, ColumnDataBean, ColumnPosition
from persistance.entity_setup import Model
from persistance.entity_setup import db

with open('config.yml', 'r') as file:
    config_data = yaml.safe_load(file).get('database', {})

engine = create_engine(
    f"postgresql://{config_data.get('username', 'postgres')}:{config_data.get('password', 'postgres')}@{config_data.get('host', 'localhost')}:{config_data.get('port', 5432)}/{config_data.get('db_name', 'postgres')}")
Session = sessionmaker(bind=engine)


def save_model_details_to_db(image_path, columns):
    session = Session()
    if image_path:
        with open(image_path, 'rb') as image_file:
            master_img = image_file.read()
            master_img_base64 = base64.b64encode(master_img).decode('utf-8')
    else:
        master_img_base64 = None

    if isinstance(columns, (dict, list)):
        columns_json = columns
    else:
        raise ValueError("Columns data must be a dictionary or list.")

    try:
        new_model = Model(trained_master_image=master_img_base64, columns=columns_json)
        session.add(new_model)
        session.commit()
        return new_model.id
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()


def get_model_from_db(model_id):
    return Model.query.get(model_id)


def get_model_from_database(model_id):
    model: Model = Model.query.get(model_id)
    if model is None:
        return None
    column_beans = prepare_column_bean(model.columns)

    return ModelBean(model.id, column_beans)


def prepare_column_bean(json_str: str):
    data = json.loads(json_str)
    columns = []
    for item in data:
        position = ColumnPosition(**item['position'])
        column = ColumnDataBean(column_name=item['columnName'], position=position)
        columns.append(column)
    return columns


def fetch_all_model():
    # all_models = db.session.query(Model).all()
    all_models = Model.query.all()
    print(all_models)
    return all_models

    # return db.session.query(Model).all()
