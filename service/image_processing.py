import cv2
from per_process.pre_processing import start_pre_process
from service.ocr import logger, fetch_values_from_paddle_ocr


def process_single_file(file_name, image_path, model_bean):
    logger.info(f"Processing file: {file_name}")
    image = cv2.imread(image_path)
    processed_image = start_pre_process(image)
    final_result_list = fetch_values_from_paddle_ocr(processed_image, model_bean.columns)
    return {"fileName": file_name, 'field_results': final_result_list}
