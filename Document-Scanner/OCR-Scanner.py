import cv2
from pdf2image import convert_from_path
import numpy as np
from paddleocr import PaddleOCR

pdf_path = r"/home/p3/IdeaProjects/OCR-Project/DepositSlip/Adobe Scan 2 Jul 2024-1.pdf"

pdf_pages = convert_from_path(pdf_path)

width_position = 750
height_position = 120
top_position = 320
left_position = 100


def is_bounding_box_within(bounding_box, position):
    x1, y1 = bounding_box[0]
    x2, y2 = bounding_box[3]

    pos_x = position['x']
    pos_y = position['y']
    pos_width = position['width']
    pos_height = position['height']

    # Check if all corners of the bounding box are within the position boundaries
    return (x1 >= pos_x and x2 <= pos_x + pos_width and
            y1 >= pos_y and y2 <= pos_y + pos_height)


def fetch_value_using_coordinates(img, top, left, width, height):
    thresh = 255 - cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    ocr = PaddleOCR(use_angle_cls=True, lang='en', det_lang='ml')
    result = ocr.ocr(thresh, cls=True)
    bb = is_bounding_box_within(result[0][0][0], {'x': top, 'y': left, 'width': width, 'height': height})
    print(bb)
    if bb:
        roi = thresh[top:top + height, left:left + width]
        res = ocr.ocr(roi, cls=True)
        print("res", res)


def process_page(page):
    img = cv2.cvtColor(np.array(page), cv2.COLOR_BGR2GRAY)
    fetch_value_using_coordinates(img, top_position, left_position, width_position, height_position)


# Process each page
for pages in pdf_pages:
    process_page(pages)
