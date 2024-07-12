import csv
from models import ColumnPosition, Bean, Response


def parse_json_to_beans(json_data):
    beans = []
    for item in json_data:
        column_name = item["columnName"]
        position_data = item["position"]
        position = ColumnPosition(**position_data)
        bean = Bean(column_name, position)
        beans.append(bean)
    return beans


def is_bounding_box_within(bounding_box, position: ColumnPosition):
    x1, y1 = bounding_box[0]
    x2, y2 = bounding_box[3]

    pos_x = position.x
    pos_y = position.y
    pos_width = position.width
    pos_height = position.height

    x = x1 >= pos_x
    y = y1 >= pos_y
    width = x2 <= pos_x + pos_width
    height = y2 <= pos_y + pos_height

    return x and width and y and height


def get_position_values(bbox):
    x_coords = [point[0] for point in bbox]
    y_coords = [point[1] for point in bbox]

    width_position = int(max(x_coords) - min(x_coords))
    height_position = int(max(y_coords) - min(y_coords))
    top_position = int(min(y_coords))
    left_position = int(min(x_coords))
    return width_position, height_position, top_position, left_position


def prepare_response(binding_name, value):
    response = Response(binding_name, value)
    print("Response ---->", response)
    return response


def write_to_csv(data, output_file='../output_sample.csv'):
    columns = [item[0] for item in data]
    values = [item[1] for item in data]

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerow(values)
        file.close()


def retrieve_results(thresh, ocr):
    result = ocr.ocr(thresh, cls=True)
    return result
