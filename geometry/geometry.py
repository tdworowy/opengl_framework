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

    def apply_matrix(self, matrix, variable_name="vertexPosition"):
        old_position_data = self.attributes[variable_name].data
        new_position_data = []

        for old_pos in old_position_data:
            new_pos = old_pos.copy()
            new_pos.append(1)
            new_pos = matrix @ new_pos
            new_pos = list(new_pos[0:3])
            new_position_data.append(new_pos)

        self.attributes[variable_name].data = new_position_data
        self.attributes[variable_name].upload_data()

    def merge(self, other_geometry):
        for variable_name, attribute_object in self.attributes.items():
            attribute_object.data += other_geometry.attributes[variable_name].data
            attribute_object.upload_data()
        self.count_vertices()
