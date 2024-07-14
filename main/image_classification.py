import pytesseract
from pytesseract import Output
import numpy as np
from skimage.metrics import structural_similarity as ssim

import cv2
import aspose.ocr as ocr
import io
from PIL import Image, ImageEnhance


def is_flipped(image):
    pil_image = Image.fromarray(image)
    d = pytesseract.image_to_osd(pil_image, output_type=Output.DICT)
    orientation = d['rotate']

    return orientation == 180


def is_blurred(image):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
    return laplacian_var < 100


def is_noisy(image):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised_image = cv2.fastNlMeansDenoising(image, None, 30, 7, 21)
    score, _ = ssim(image, denoised_image, full=True)
    return score < 0.9


def perform_de_blurring(image):
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(blurred_image, -1, sharpening_kernel)

    pil_image = Image.fromarray(sharpened_image)

    enhancer = ImageEnhance.Contrast(pil_image)
    return enhancer.enhance(2)


def image_classify_and_pre_process(image):
    flipped = is_flipped(image)
    if flipped:
        image = skewing(image)
        cv2.imwrite("output_folder/flip.png", image)

    blurred = is_blurred(image)
    if blurred:
        image = perform_de_blurring(image)
        cv2.imwrite("/home/p3/IdeaProjects/OCR-Project/resources/output_folder/test1.png", image)

    noisy = is_noisy(image)
    if noisy:
        pass

    print(f'Flipped: {flipped}, Blurred: {blurred}, Noisy: {noisy}')
    return image


def skewing(cv2_image):
    filters = ocr.models.preprocessingfilters.PreprocessingFilter()
    filters.add(filters.AutoSkew())

    img = ocr.OcrInput(ocr.InputType.SINGLE_IMAGE, filters)
    img.add(cv2_image)

    skewed_pil_image = Image.open(io.BytesIO(img))
    skewed_cv2_image = pil_to_cv2(skewed_pil_image)

    return skewed_cv2_image


def cv2_to_pil(cv2_img):
    color_conversion = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_conversion)
    return pil_image


def pil_to_cv2(pil_img):
    np_img = np.array(pil_img)
    open_cv_image = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    return open_cv_image
