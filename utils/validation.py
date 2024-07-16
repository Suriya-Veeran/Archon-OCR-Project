import os
import logging

logger = logging.getLogger('ppocr')


def validate_directory(input_directory_path):
    if not os.path.isdir(input_directory_path):
        logger.error(f"The path '{input_directory_path}' is not a directory.")
        return False

    if not os.listdir(input_directory_path):
        logger.error(f"The directory '{input_directory_path}' is empty.")
        return False

    return True


def is_image_file(file_name):
    return file_name.lower().endswith(('.png', '.jpg', '.jpeg'))
