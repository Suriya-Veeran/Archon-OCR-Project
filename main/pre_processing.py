import cv2


def start_pre_process(image):
    original_dimensions = (image.shape[1], image.shape[0])

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)

    resized_image = cv2.resize(thresholded_image, original_dimensions, interpolation=cv2.INTER_LINEAR)
    resized_image_size = (resized_image.shape[1], resized_image.shape[0])

    return resized_image
