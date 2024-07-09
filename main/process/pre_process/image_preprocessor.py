import cv2
import numpy as np
from PIL import Image
import tempfile


def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    angle = -(90 + angle) if angle < -45 else -angle
    h, w = image.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def normalize_image(img):
    return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)


def set_image_dpi(file_path):
    with Image.open(file_path) as im:
        factor = min(1, 1024.0 / im.size[0])
        size = (int(factor * im.size[0]), int(factor * im.size[1]))
        im_resized = im.resize(size, Image.ANTIALIAS)
        temp_filename = tempfile.NamedTemporaryFile(delete=False, suffix='.png').name
        im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename


def remove_noise(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)


def thin_image(image_path):
    img = cv2.imread(image_path, 0)
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)
    ret, img = cv2.threshold(img, 127, 255, 0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    while cv2.countNonZero(img) != 0:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        skel = cv2.bitwise_or(skel, cv2.subtract(img, temp))
        img = eroded.copy()
    return skel


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def preprocess_image(file_path):
    temp_path = set_image_dpi(file_path)
    img = cv2.imread(temp_path)
    img = remove_noise(img)
    img = get_grayscale(img)
    img = normalize_image(img)
    img = deskew(img)
    img = thresholding(img)
    preprocessed_image_path = tempfile.NamedTemporaryFile(delete=False, suffix='.png').name
    cv2.imwrite(preprocessed_image_path, img)
    return preprocessed_image_path


