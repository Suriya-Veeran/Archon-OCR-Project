from pdf2image import convert_from_path
from pytesseract import image_to_data

path_to_pdf = r"/home/p3/IdeaProjects/OCR-Project/Document-PDF/deposit slip.pdf"

# Add Tesseract directory to PATH if not already added
# tesseract_path = r'usr/bin:tesseract'
# if tesseract_path not in os.environ['PATH']:
#     os.environ['PATH'] = tesseract_path + ';' + os.environ['PATH']

# # Add Poppler bin directory to PATH if not already added
# poppler_path = r'C:\Users\P3INW82\Downloads\Release-24.02.0-0\poppler-24.02.0\Library\bin'
# if poppler_path not in os.environ['PATH']:
#     os.environ['PATH'] = poppler_path + ';' + os.environ['PATH']


def convert_pdf_to_img(pdffile):
    return convert_from_path(pdffile)


def convert_image_to_text(file):
    text = image_to_data(file, output_type='dict')
    return text


def get_text_from_pdf(pdffile):
    images = convert_pdf_to_img(pdffile)
    final_text = ""
    for pg, img in enumerate(images):
        print(convert_image_to_text(img))
    return final_text


print(get_text_from_pdf(path_to_pdf))
