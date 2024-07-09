import cv2
import numpy as np
from pdf2image import convert_from_path

from image_preprocessor import ImagePreprocessor
from ocr_processing import fetch_value_using_coordinates



def process_image(image_path, bean):
    preprocessor = ImagePreprocessor()
    processed_image_path = preprocessor.preprocess_image(image_path)
    print(f"Preprocessed image saved at: {processed_image_path}")
    # image = cv2.imread(processed_image_path)
    # print(type(image))
    # pre_processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # print(type(pre_processed_image))
    fetch_value_using_coordinates(processed_image_path, bean)


def convert_pdf_to_images(pdf_path):
    return convert_from_path(pdf_path)


def process_page(page, bean):
    img = cv2.cvtColor(np.array(page), cv2.COLOR_BGR2GRAY)
    fetch_value_using_coordinates(img, bean)
