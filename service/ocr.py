import logging
import cv2
from paddleocr import PaddleOCR
from utils.utils import retrieve_results, is_bounding_box_within

logger = logging.getLogger('ppocr')


def fetch_values_from_paddle_ocr(img, beans):
    thresh = preprocess_image_for_ocr(img)
    ocr = initialize_paddle_ocr()

    final_result_list = process_ocr_results(thresh, ocr, beans)

    logger.info(final_result_list)
    return final_result_list


def preprocess_image_for_ocr(img):
    return 255 - cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


def initialize_paddle_ocr():
    return PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)


def process_ocr_results(thresh, ocr, beans):
    result = retrieve_results(thresh, ocr)
    logger.info(result)
    final_result_list = []

    for res in result[0]:
        bbox = res[0]
        for bean in beans:
            if is_bounding_box_within(bbox, bean.position) and res[0] and res[1]:
                accuracy = res[1][1]
                if accuracy > 0.50:
                    value = res[1][0]
                    final_result = {'binding_name': bean.column_name, 'value': value}
                    final_result_list.append(final_result)

    return final_result_list
