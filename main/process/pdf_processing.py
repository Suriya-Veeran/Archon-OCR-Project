import cv2
import numpy as np
from pdf2image import convert_from_path

from main.process.pre_process.image_preprocessor import ImagePreprocessor
from ocr_processing import fetch_value_using_coordinates


def process_image(image_path, bean):
    preprocessor = ImagePreprocessor()
    processed_image_path = preprocessor.preprocess_image(image_path)
    print(f"Preprocessed image saved at: {processed_image_path}")
    fetch_value_using_coordinates(processed_image_path, bean)


def convert_pdf_to_images(pdf_path):
    return convert_from_path(pdf_path)


def process_page(page, bean):
    img = cv2.cvtColor(np.array(page), cv2.COLOR_BGR2GRAY)
    fetch_value_using_coordinates(img, bean)
