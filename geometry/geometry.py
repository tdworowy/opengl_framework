from core.attribute import Attribute
from core.data_type import DataType


class Geometry:

    def __init__(self):
        self.attributes = {}
        self.vertex_count = None

    def add_attribute(self, data_type: DataType,
                      variable_name: str, data: list[list[float]]):
        self.attributes[variable_name] = Attribute(data_type, data)

    def count_vertices(self):
        attrib = list(self.attributes.values())[0]
        self.vertex_count = len(attrib.data)
