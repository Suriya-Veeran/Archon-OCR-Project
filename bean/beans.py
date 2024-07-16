from collections.abc import Iterable


class ColumnPosition:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return f"ColumnPosition(x={self.x}, y={self.y}, width={self.width}, height={self.height})"

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }


class ColumnDataBean:
    def __init__(self, column_name, position: ColumnPosition):
        self.column_name = column_name
        self.position = position

    def to_dict(self):
        return {
            "columnName": self.column_name,
            "position": self.position.to_dict()
        }


class ModelBean:
    def __init__(self, model_id, columns: Iterable[ColumnDataBean]):
        self.id = model_id
        self.columns = columns

    def to_dict(self):
        return {
            "id": self.id,
            "columns": [column.to_dict() for column in self.columns]
        }

