# import cv2
# from pdf2image import convert_from_path
# import numpy as np
# from paddleocr import PaddleOCR
#
# pdf_path = r"/home/p3/IdeaProjects/OCR-Project/DepositSlip/Adobe Scan 2 Jul 2024-1.pdf"
#
# pdf_pages = convert_from_path(pdf_path)
#
# width_position = 1400
# height_position = 809
# top_position = 100
# left_position = 98
#
#
# def is_bounding_box_within(bounding_box, position):
#     x1, y1 = bounding_box[0]
#     x2, y2 = bounding_box[3]
#
#     pos_x = position['x']
#     pos_y = position['y']
#     pos_width = position['width']
#     pos_height = position['height']
#
#     # Check if all corners of the bounding box are within the position boundaries
#     return (x1 >= pos_x and x2 <= pos_x + pos_width and
#             y1 >= pos_y and y2 <= pos_y + pos_height)
#
#
# def get_values(bbox):
#     # Extract x and y coordinates
#     x_coords = [point[0] for point in bbox]
#     y_coords = [point[1] for point in bbox]
#
#     # Calculate width, height, top, and left positions
#     width_position = int(max(x_coords) - min(x_coords))
#     height_position = int(max(y_coords) - min(y_coords))
#     top_position = int(min(y_coords))
#     left_position = int(min(x_coords))
#     return width_position, height_position, top_position, left_position
#
#
# def fetch_value_using_coordinates(img, top, left, width, height):
#     thresh = 255 - cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#
#     ocr = PaddleOCR(use_angle_cls=True, lang='en', det_lang='ml')
#     result = ocr.ocr(thresh, cls=True)
#     for i in range(len(result[0])):
#         i_ = result[0][i][0]
#         flag = is_bounding_box_within(i_, {'x': top, 'y': left, 'width': width, 'height': height})
#         if flag:
#             width_position, height_position, top_position, left_position = get_values(i_)
#             position = top_position + height_position
#             position_width_position = left_position + width_position
#             roi = thresh[top_position:position, left_position:position_width_position]
#             res = ocr.ocr(roi, cls=True)
#             print("res", res)
#
#
# def process_page(page):
#     img = cv2.cvtColor(np.array(page), cv2.COLOR_BGR2GRAY)
#     fetch_value_using_coordinates(img, top_position, left_position, width_position, height_position)
#
#
# # Process each page
# for pages in pdf_pages:
#     process_page(pages)
#
#
#
#
#
#
#
# import json
#
#
# class ColumnPosition:
#     def __init__(self, x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#
#     def __repr__(self):
#         return f"ColumnPosition(x={self.x}, y={self.y}, width={self.width}, height={self.height})"
#
#
# class Bean:
#     def __init__(self, columnName, position):
#         self.columnName = columnName
#         self.position = position
#
#     def __repr__(self):
#         return f"Bean(columName={self.columnName}, position={self.position})"
#
#
# def parse_json_to_bean(json_data):
#     beans = []
#     for item in json_data:
#         columName = item["columnName"]
#         position_data = item["position"]
#         position = ColumnPosition(**position_data)
#         bean = Bean(columName, position)
#         beans.append(bean)
#     return beans
#
#
# # Example JSON input as a string
# json_string = '''
# [
#     {
#         "columnName": "accountName",
#         "position": {
#             "x": 101,
#             "y": 12,
#             "width": 100,
#             "height": 200
#         }
#     },
#     {
#         "columnName": "amount",
#         "position": {
#             "x": 101,
#             "y": 12,
#             "width": 100,
#             "height": 200
#         }
#     }
# ]
# '''
#
#
#
# # Parse the JSON string
# json_data = json.loads(json_string)
#
# # Convert JSON to Bean objects
# beans = parse_json_to_bean(json_data)
#
# # Output the parsed beans
# for bean in beans:
#     print(bean)
#
