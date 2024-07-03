import cv2
import pytesseract
from pdf2image import convert_from_path
import numpy as np

pdf_path = r"/home/p3/IdeaProjects/OCR-Project/DepositSlip/Adobe Scan 2 Jul 2024-1.pdf"

# Convert PDF to images
pages = convert_from_path(pdf_path)

width = 202
height = 58
top = 115
left = 143


def convert_image_to_text(file):
    text = pytesseract.image_to_data(file, output_type='dict')  # each input
    #iterate_the_values(text)
    return text


def iterate_the_values(text):
    for i, block in enumerate(text['level']):
        values = {
            "level": text["level"][i],
            "page_num": text["page_num"][i],
            "block_num": text["block_num"][i],
            "par_num": text["par_num"][i],
            "line_num": text["line_num"][i],
            "word_num": text["word_num"][i],
            "left": text["left"][i],
            "top": text["top"][i],
            "width": text["width"][i],
            "height": text["height"][i],
            "conf": text["conf"][i],
            "text": text["text"][i]
        }

        print(values)
        print(values.get('text'))


def iterate_the_data_using_coordinates(data):
    for i, (text, left, top, width, height) in enumerate(
            zip(data['text'], data['left'], data['top'], data['width'], data['height'])):
        if text.strip():  # Ensure it's not an empty string

            print(f"Text: {text}, Left: {left}, Top: {top}, Width: {width}, Height: {height}")


def fetch_value_using_coordinates(img, top, left, width, height):
    # roi
    roi = img[top:top + height, left:left + width]
    print(top)
    print(top+height)
    print(left)
    print(left+width)
    text = pytesseract.image_to_string(roi)
    print("text ---> ", text)
    # return text


def process_page(page):
    img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
    data = convert_image_to_text(img)
    iterate_the_data_using_coordinates(data)
    #fetch_value_using_coordinates(img, top, left, width, height)


# Process each page
for page in pages:
    process_page(page)
