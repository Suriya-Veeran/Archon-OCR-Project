import cv2
import numpy as np
from pdf2image import convert_from_path
from ocr_processing import fetch_value_using_coordinates
from over_all_test import preprocess_image


def convert_pdf_to_images(pdf_path):
    return convert_from_path(pdf_path)


def process_page(page, bean):
    img = cv2.cvtColor(np.array(page), cv2.COLOR_BGR2GRAY)
    fetch_value_using_coordinates(img, bean)


def process_image(img, bean):
    pre_processed_image = preprocess_image(img)
    fetch_value_using_coordinates(pre_processed_image, bean)
