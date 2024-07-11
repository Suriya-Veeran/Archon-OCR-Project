import json

import cv2

from data_classes import parse_json_to_bean
from ocr_processing import fetch_value_using_coordinates

img_path = r"/home/p3/IdeaProjects/OCR-Project/resources/images/test.png"
json_Sample = '''
    [
    {
        "columnName": "depositor",
        "position": {
          "x": 56,
          "y": 305,
          "width": 67,
          "height": 22
        }
      }
       ,
      {
        "columnName": "date",
        "position": {
          "x": 95,
          "y": 92,
          "width": 233,
          "height": 37
        }
      }
      ,
      {
        "columnName": "amount name",
        "position": {
          "x": 148,
          "y": 519,
          "width": 284,
          "height": 40
        }
      } 
    ]   
    '''
json_data = json.loads(json_Sample)
beans = parse_json_to_bean(json_data)


def process_image(image_path):
    # preprocessor = ImagePreprocessor()
    # processed_image_path = preprocessor.preprocess_image(image_path)

    image = cv2.imread(image_path)
    processed_image_path = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return processed_image_path


processed_image_path = process_image(img_path)
fetch_value_using_coordinates(processed_image_path, beans)

# for bean in beans:
#     fetch_value_using_coordinates(processed_image_path, bean)
