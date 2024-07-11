import cv2

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import interpolation as inter


def analyze_image(image):
    if len(image.shape) == 2:
        gray_image = image
    else:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    noise_level = np.std(gray_image)

    contrast = np.max(gray_image) - np.min(gray_image)

    return gray_image, noise_level, contrast


def retrieve_binary_image(image, image_path):
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    gray_image, noise_level, contrast = analyze_image(image)
    if noise_level > 30:
        print("Applying Gaussian Blur to reduce noise")
        gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    if contrast < 50:
        print("Enhancing contrast using histogram equalization")
        gray_image = cv2.equalizeHist(gray_image)
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return binary_image


def needs_grayscale(image):
    return len(image.shape) == 3 and image.shape[2] == 3


def needs_denoising(image):
    noise_level = cv2.Laplacian(image, cv2.CV_64F).var()
    return noise_level > 100  # Example threshold


def needs_de_skewing(image):
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    if lines is None:
        return False
    angles_ = [np.arctan2(np.sin(theta), np.cos(theta)) * 180 / np.pi for rho, theta in lines[:, 0]]
    mean_angle = np.mean(angles_)
    return abs(mean_angle) > 1  # Example threshold


def needs_thresholding(image):
    contrast = image.max() - image.min()
    return contrast < 50  # Example threshold


def needs_perspective_transformation(image):
    corners = cv2.goodFeaturesToTrack(image, maxCorners=4, qualityLevel=0.01, minDistance=30)
    return corners is not None and len(corners) == 4


def start_pre_process(image):

    # Step 2: Convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 3: Noise reduction (using Gaussian Blur)
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Step 4: Adaptive thresholding
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Step 5: Skew correction
    image = skew_correction(image)

    # Optional: Additional preprocessing steps (e.g., morphological operations)
    # kernel = np.ones((3, 3), np.uint8)
    # image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    return image

def skew_correction(image):
    # Invert the image colors
    image = cv2.bitwise_not(image)

    # Find coordinates of all non-zero pixels
    coords = np.column_stack(np.where(image > 0))

    # Compute the minimum area bounding box
    angle = cv2.minAreaRect(coords)[-1]

    # Adjust the angle
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Rotate the image to correct the skew
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    corrected_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # Invert the image colors back
    corrected_image = cv2.bitwise_not(corrected_image)

    return corrected_image

def find_score(arr, angle):
    data = inter.rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score


def skew_correction(img):
    wd, ht = img.shape
    pix = np.array(img, np.uint8)
    bin_img = 1 - (pix / 255.0)
    plt.imshow(bin_img, cmap='gray')
    plt.savefig('binary.png')
    delta = 1
    limit = 5
    angles = np.arange(-limit, limit + delta, delta)
    scores = []
    for angle in angles:
        hist, score = find_score(bin_img, angle)
        scores.append(score)
    best_score = max(scores)
    best_angle = angles[scores.index(best_score)]
    print('Best angle: {}'.format(best_angle))
    # Correct skew
    data = inter.rotate(bin_img, -5, reshape=False, order=0)
    corrected_image = (255 * data).astype("uint8")
    return corrected_image


def find_score(arr, angle):
    data = inter.rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score


