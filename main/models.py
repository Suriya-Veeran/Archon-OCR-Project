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
        return f"Bean(column_name={self.column_name}, position={self.position})"


class Response:
    def __init__(self, binding_name, value):
        self.binding_name = binding_name
        self.value = value

    def __repr__(self):
        return f"Response(binding_name={self.binding_name}, value={self.value})"
