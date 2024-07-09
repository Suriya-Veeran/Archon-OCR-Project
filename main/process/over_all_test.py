import cv2
import numpy as np


def preprocess_image(image_path):
    print("img-path -----> ", image_path)
    target_height = 32
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Step 1: Noise Removal
    img = cv2.medianBlur(img, 3)  # Median filtering

    # Step 2: Thresholding
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Step 3: Deskewing (optional)
    coords = np.column_stack(np.where(img > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # Step 4: Denoising (optional)
    img = cv2.fastNlMeansDenoising(img, None, h=10, templateWindowSize=7, searchWindowSize=21)

    # Step 5: Resize to target height while maintaining aspect ratio
    scale = target_height / img.shape[0]
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)


    # Step 6: Unsharp masking
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.addWeighted(img, 1.5, blurred, -0.5, 0)


    # Step 7: Masking (optional)
    # Create a circular mask
    mask = np.zeros_like(img)
    center = (img.shape[1] // 2, img.shape[0] // 2)
    radius = min(center[0], center[1])
    cv2.circle(mask, center, radius, 255, -1)
    img = cv2.bitwise_and(img, mask)

    cv2.imwrite("final-image/pre-processing.png", img)
    return img



