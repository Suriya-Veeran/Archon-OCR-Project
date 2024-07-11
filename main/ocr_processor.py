
import logging

import cv2
from paddleocr import PaddleOCR

from config import IMG_PATH
from pre_processing import start_pre_process
from utils import is_bounding_box_within, get_position_values, prepare_response, write_to_csv, retrieve_results

logging.basicConfig(level=logging.ERROR)


logger = logging.getLogger('ppocr')
logger.setLevel(logging.ERROR)


def start_process(beans):
    processed_image = process_image(IMG_PATH)
    fetch_value_using_coordinates(processed_image, beans)

def process_image(image_path):
    image = cv2.imread(image_path)

    # binary_image = retrieve_binary_image(image, image_path)
    binary_image = start_pre_process(image)
    cv2.imwrite("sampleeeee.png",binary_image)
    return binary_image

    # if image is None:
    #     raise FileNotFoundError(f"Image not found at path: {image_path}")
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # return gray_image


def fetch_value_using_coordinates(img, beans):
    thresh = 255 - cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    extracted_data = []

    for bean in beans:
        result = retrieve_results(thresh, ocr)
        print(result)
        for res in result[0]:
            bbox = res[0]
            if is_bounding_box_within(bbox, bean.position):
                width_position, height_position, top_position, left_position = get_position_values(bbox)
                position = top_position + height_position
                position_width_position = left_position + width_position
                roi = thresh[top_position:position, left_position:position_width_position]
                ocr_res = ocr.ocr(roi, cls=True)
                if ocr_res and ocr_res[0]:
                    value = ocr_res[0][0][1][0]
                    accuracy = ocr_res[0][0][1][1]
                    if accuracy > 0.75:
                        prepare_response(bean.column_name, value)
                        extracted_data.append((bean.column_name, value))

    write_to_csv(extracted_data)



