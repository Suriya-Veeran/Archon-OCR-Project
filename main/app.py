import json

from flask import Flask, request, jsonify

from config import JSON_SAMPLE
from ocr_processor import start_process
from utils import parse_json_to_beans

app = Flask(__name__)


@app.route('/process', methods=['POST'])
def process_input_with_model():
    json_data = json.loads(JSON_SAMPLE)
    beans = parse_json_to_beans(json_data)
    start_process(beans)
    return "success"


if __name__ == '__main__':
    app.run(debug=True)
