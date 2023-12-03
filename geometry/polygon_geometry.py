from core.data_type import DataType
from geometry.geometry import Geometry
from math import sin, cos, pi


class PolygonGeometry(Geometry):
    def __init__(self, sides=3, radius=1):
        super().__init__()
        A = 2 * pi / sides
        position_data = []
        color_data = []

        for n in range(sides):
            position_data.append([0, 0, 0])
            position_data.append([radius * cos(n * A), radius * sin(n * A), 0])
            position_data.append(
                [radius * cos((n + 1) * A), radius * sin((n + 1) * A), 0])

            color_data.append([1, 1, 1])
            color_data.append([1, 0, 0])
            color_data.append([0, 0, 1])

        self.add_attribute(DataType.vec3, "vertexPosition", position_data)
        self.add_attribute(DataType.vec3, "vertexColor", color_data)

        self.count_vertices()
