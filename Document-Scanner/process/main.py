import json
from pdf_processing import convert_pdf_to_images, process_page
from data_classes import parse_json_to_bean

pdf_path = r"/home/p3/IdeaProjects/OCR-Project/DepositSlip/Adobe Scan 2 Jul 2024-1.pdf"
json_string = '''
[
    {
        "columnName": "accountName",
        "position": {
            "x": 141,
            "y": 102,
            "width": 315,
            "height": 80
        }
    },
    {
    "columnName": "amount name",
        "position": {
            "x": 18,
            "y": 40,
            "width": 205,
            "height": 50
        }
    },
    {
    "columnName": "signature",
        "position": {
            "x": 616,
            "y": 1720,
            "width": 130,
            "height": 40
        }
    }
    
]
'''

# Parse the JSON string
json_data = json.loads(json_string)

# Convert JSON to Bean objects
beans = parse_json_to_bean(json_data)

# PDF processing
pdf_pages = convert_pdf_to_images(pdf_path)

# Output the parsed beans
for bean in beans:
    for page in pdf_pages:
        process_page(page, bean)
