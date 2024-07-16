import logging
import os

from flask import abort, jsonify

from service.image_processing import process_single_file
from persistance.model_repository import save_model_details_to_db, fetch_all_model, get_model_from_database
from utils.validation import validate_directory, is_image_file

logger = logging.getLogger('ppocr')


def save_model_details(data):
    image = data.get('image')
    columns = data.get('columns', [])

    model_id = save_model_details_to_db(image, columns)
    return model_id


def process_input_data_with_model(model_bean, input_directory_path):
    if not validate_directory(input_directory_path):
        return

    results = []

    for file_name in os.listdir(input_directory_path):
        image_path = os.path.join(input_directory_path, file_name)
        if os.path.isfile(image_path) and is_image_file(file_name):
            result = process_single_file(file_name, image_path, model_bean)
            if result:
                results.append(result)

    return results


def process_files_with_model(model_id, input_folder_path):
    model_bean = get_model_from_database(model_id)
    if model_bean is None:
        abort(404, description="Model not found")

    results = process_input_data_with_model(model_bean, input_folder_path)

    return jsonify(results)


def all_models():
    return fetch_all_model()
