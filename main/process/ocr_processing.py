import csv
import logging

import cv2
from paddleocr import PaddleOCR

from data_classes import prepare_response_bean

# Configure the root logger
logging.basicConfig(level=logging.ERROR)

# Configure the PaddleOCR logger
logger = logging.getLogger('ppocr')
logger.setLevel(logging.ERROR)


def is_bounding_box_within(bounding_box, position):
    x1, y1 = bounding_box[0]
    x2, y2 = bounding_box[3]

    pos_x = position['x']
    pos_y = position['y']
    pos_width = position['width']
    pos_height = position['height']

    return (x1 >= pos_x and x2 <= pos_x + pos_width and
            y1 >= pos_y and y2 <= pos_y + pos_height)


def get_position_values(bbox):
    x_coords = [point[0] for point in bbox]
    y_coords = [point[1] for point in bbox]

    width_position = int(max(x_coords) - min(x_coords))
    height_position = int(max(y_coords) - min(y_coords))
    top_position = int(min(y_coords))
    left_position = int(min(x_coords))
    return width_position, height_position, top_position, left_position


def retrieve_results(thresh, ocr):
    result = ocr.ocr(thresh, cls=True)
    print(result)
    return result


def write_to_csv(data):
    columns = [item[0] for item in data]
    values = [item[1] for item in data]

    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerow(values)



def fetch_value_using_coordinates(img, beans):
    thresh = 255 - cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    ocr = PaddleOCR(use_angle_cls=True, lang='en', det_lang='ml')
    # ocr = PaddleOCR(use_angle_cls=True, lang='en', det_lang='ml')
    # result = ocr.ocr(thresh, cls=True)
    # print(result)
    extracted_data = []

    for bean in beans:
        result = retrieve_results(thresh, ocr)
        width = bean.position.width
        height = bean.position.height
        top = bean.position.x
        left = bean.position.y


        for i in range(len(result[0])):
            i_ = result[0][i][0]
            flag = is_bounding_box_within(i_, {'x': top, 'y': left, 'width': width, 'height': height})
            if flag:
                width_position, height_position, top_position, left_position = get_position_values(i_)
                position = top_position + height_position
                position_width_position = left_position + width_position
                roi = thresh[top_position:position, left_position:position_width_position]
                cv2.imwrite("sample.png", roi)
                res = ocr.ocr(roi, cls=True)
                if res[0] is None:
                    print("OCR failed to recognize text in ROI")
                else:
                    accuracy = res[0][0][1][1]
                    if accuracy > 0.75:
                        value = res[0][0][1][0]
                        prepare_response_bean(bean.column_name, value)
                        extracted_data.append((bean.column_name, value))

    # Write the accumulated data to CSV
    write_to_csv(extracted_data)