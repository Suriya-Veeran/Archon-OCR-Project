import json
from main.process.data_classes import parse_json_to_bean
from main.process.pdf_processing import process_image

if __name__ == "__main__":
    img_path = r"/resources/img.png"
    json_Sample = '''
    [
      {
        "columnName": "data binding",
        "position": {
          "x": 100,
          "y": 82,
          "width": 221,
          "height": 55
        }
      }
    ] 
    '''
    json_data = json.loads(json_Sample)
    beans = parse_json_to_bean(json_data)
    for bean in beans:
        process_image(img_path, bean)
