import cv2
import numpy as np
from PIL import Image
import tempfile
import logging

class ImagePreprocessor:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def normalize_image(self, img):
        try:
            self.logger.info("Normalizing image")
            return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        except Exception as e:
            self.logger.error(f"Error in normalizing image: {e}")
            raise

    def deskew(self, image):
        try:
            self.logger.info("Deskewing image")
            co_ords = np.column_stack(np.where(image > 0))
            angle = cv2.minAreaRect(co_ords)[-1]
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            return rotated
        except Exception as e:
            self.logger.error(f"Error in deskewing image: {e}")
            raise

    def set_image_dpi(self, file_path):
        try:
            self.logger.info("Setting image DPI")
            im = Image.open(file_path)
            length_x, width_y = im.size
            factor = min(1, float(1024.0 / length_x))
            size = int(factor * length_x), int(factor * width_y)
            im_resized = im.resize(size, Image.LANCZOS)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            temp_filename = temp_file.name
            im_resized.save(temp_filename, dpi=(300, 300))
            return temp_filename
        except Exception as e:
            self.logger.error(f"Error in setting image DPI: {e}")
            raise

    def remove_noise(self, image):
        try:
            self.logger.info("Removing noise from image")
            return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)
        except Exception as e:
            self.logger.error(f"Error in removing noise: {e}")
            raise

    def thin_image(self, image_path):
        try:
            self.logger.info("Thinning image")
            img = cv2.imread(image_path, 0)
            size = np.size(img)
            skel = np.zeros(img.shape, np.uint8)

            ret, img = cv2.threshold(img, 127, 255, 0)
            element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
            done = False

            while not done:
                eroded = cv2.erode(img, element)
                temp = cv2.dilate(eroded, element)
                temp = cv2.subtract(img, temp)
                skel = cv2.bitwise_or(skel, temp)
                img = eroded.copy()

                zeros = size - cv2.countNonZero(img)
                if zeros == size:
                    done = True

            return skel
        except Exception as e:
            self.logger.error(f"Error in thinning image: {e}")
            raise

    def get_grayscale(self, image):
        try:
            self.logger.info("Converting image to grayscale")
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            self.logger.error(f"Error in converting to grayscale: {e}")
            raise

    def thresholding(self, image):
        try:
            self.logger.info("Applying thresholding to image")
            return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        except Exception as e:
            self.logger.error(f"Error in thresholding: {e}")
            raise

    def preprocess_image(self, file_path):
        try:
            self.logger.info("Starting image preprocessing pipeline")

            temp_path = self.set_image_dpi(file_path)
            img = cv2.imread(temp_path)
            img = self.remove_noise(img)
            img = self.get_grayscale(img)
            img = self.normalize_image(img)
            img = self.deskew(img)
            img = self.thresholding(img)
            preprocessed_image_path = tempfile.NamedTemporaryFile(delete=False, suffix='.png').name
            print(preprocessed_image_path)
            cv2.imwrite(preprocessed_image_path, img)
            self.logger.info("Image preprocessing complete")
            return img
        except Exception as e:
            self.logger.error(f"Error in preprocessing image: {e}")
            raise

