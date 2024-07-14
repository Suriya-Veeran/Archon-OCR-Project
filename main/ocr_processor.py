import logging
import os

import cv2
from paddleocr import PaddleOCR

from pre_processing import start_pre_process
from utils import (is_bounding_box_within,
                   get_position_values, retrieve_results, parse_json_to_beans)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('ppocr')
logger.setLevel(logging.ERROR)


def process_input_folder(folder_path,
                         image_folder,
                         json_data):
    results = []
    for file_name in os.listdir(image_folder):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, file_name)

            input_beans = parse_json_to_beans(json_data)
            final_result_list = start_process(image_path, input_beans, file_name)

            single_image_result = {"fileName": file_name, 'field_results': final_result_list}

            results.append(single_image_result)
    return results


def start_process(image_path,
                  beans):
    image = cv2.imread(image_path)
    processed_image = start_pre_process(image)

    # write sample data for testing
    cv2.imwrite("./test.png", processed_image)

    return fetch_values(processed_image, beans)


def fetch_values(img,
                 beans):
    thresh = 255 - cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
    # use_gpu=False  -> for windows

    final_result_list = []

    result = retrieve_results(thresh, ocr)
    print(result)
    for res in result[0]:
        bbox = res[0]
        for bean in beans:
            if is_bounding_box_within(bbox, bean.position):

                width_position, height_position, top_position, left_position = get_position_values(bbox)
                position = top_position + height_position
                position_width_position = left_position + width_position
                roi = thresh[top_position:position, left_position:position_width_position]

                cv2.imwrite("roi-img.png", roi)
                ocr_res = ocr.ocr(roi, cls=True)

                if ocr_res and ocr_res[0]:
                    accuracy = ocr_res[0][0][1][1]
                    if accuracy > 0.75:
                        value = ocr_res[0][0][1][0]
                        final_result = {'binding_name': bean.column_name, 'value': value}
                        final_result_list.append(final_result)
    print(final_result_list)
    return final_result_list
