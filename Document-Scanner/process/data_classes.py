class ColumnPosition:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return f"ColumnPosition(x={self.x}, y={self.y}, width={self.width}, height={self.height})"


class Bean:
    def __init__(self, column_name, position: ColumnPosition):
        self.column_name = column_name
        self.position = position

    def __repr__(self):
        return f"Bean(columnName={self.column_name}, position={self.position})"


def parse_json_to_bean(json_data):
    beans = []
    for item in json_data:
        column_name = item["columnName"]
        position_data = item["position"]
        position = ColumnPosition(**position_data)
        bean = Bean(column_name, position)
        beans.append(bean)
    return beans


class Response:
    def __init__(self, binding_name, value):
        self.binding_name = binding_name
        self.value = value

    def __repr__(self):
        return f"Bean(binding_name={self.binding_name}, value={self.value})"


def prepare_response_bean(binding_name, value):
    res = Response(binding_name, value)
    print(res)




