from pdf2image import convert_from_path
from pytesseract import image_to_data
from pytesseract import image_to_string
from pytesseract import image_to_boxes
import cv2
import pytesseract

path_to_pdf = r"/home/p3/IdeaProjects/OCR-Project/Document-PDF/deposit slip.pdf"


def convert_pdf_to_img(pdffile):
    return convert_from_path(pdffile)


def convert_image_to_text(file):
    text = image_to_data(file, output_type='dict')  # each input
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


def get_text_from_pdf(pdffile):
    images = convert_pdf_to_img(pdffile)
    for pg, img in enumerate(images):
        print(convert_image_to_text(img))


#print(get_text_from_pdf(path_to_pdf))

def convert_pdf_to_img_using_opencv(path_to_pdf):
    pages = convert_from_path(path_to_pdf)

    for page in pages:
        page.save("page_image.jpg", "jpg")

    return "page_image.jpg"




def using_open_cv(path_to_pdf):
    img = convert_pdf_to_img_using_opencv(path_to_pdf)
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    text = pytesseract.image_to_string(thresh)
    print(text)


# print(using_open_cv(r"/home/p3/IdeaProjects/OCR-Project/Document-PDF/Screenshot from 2024-07-01 18-25-26.png"))
print(using_open_cv(path_to_pdf))
