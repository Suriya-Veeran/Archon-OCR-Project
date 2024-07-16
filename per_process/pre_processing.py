import cv2


def start_pre_process(image):
    original_dimensions = (image.shape[1], image.shape[0])

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)

    resized_image = cv2.resize(threshold_image, original_dimensions, interpolation=cv2.INTER_LINEAR)

    return resized_image
