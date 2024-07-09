import json

from data_classes import parse_json_to_bean
from pdf_processing import process_image


img_path = r"/home/p3/IdeaProjects/OCR-Project/resources/img_1.png"
json_Sample = '''
    [
      {
        "columnName": "data binding",
        "position": {
          "x": 0,
          "y": 0,
          "width": 223,
          "height": 223
        }
      }
    ] 
    '''
json_data = json.loads(json_Sample)
beans = parse_json_to_bean(json_data)
for bean in beans:
    process_image(img_path, bean)
