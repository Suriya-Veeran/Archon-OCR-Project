# import json
#
#
# class ColumnPosition:
#     def __init__(self, x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#
#     def __repr__(self):
#         return f"ColumnPosition(x={self.x}, y={self.y}, width={self.width}, height={self.height})"
#
#
# class Bean:
#     def __init__(self, columnName, position):
#         self.columnName = columnName
#         self.position = position
#
#     def __repr__(self):
#         return f"Bean(columName={self.columnName}, position={self.position})"
#
#
# def parse_json_to_bean(json_data):
#     beans = []
#     for item in json_data:
#         columName = item["columnName"]
#         position_data = item["position"]
#         position = ColumnPosition(**position_data)
#         bean = Bean(columName, position)
#         beans.append(bean)
#     return beans
#
#
# # Example JSON input as a string
# json_string = '''
# [
#     {
#         "columnName": "accountName",
#         "position": {
#             "x": 101,
#             "y": 12,
#             "width": 100,
#             "height": 200
#         }
#     },
#     {
#         "columnName": "amount",
#         "position": {
#             "x": 101,
#             "y": 12,
#             "width": 100,
#             "height": 200
#         }
#     }
# ]
# '''
#
#
#
# # Parse the JSON string
# json_data = json.loads(json_string)
#
# # Convert JSON to Bean objects
# beans = parse_json_to_bean(json_data)
#
# # Output the parsed beans
# for bean in beans:
#     print(bean)
