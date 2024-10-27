from core.data_type import DataType
from geometry.geometry import Geometry


class RectangleGeometry(Geometry):

    def __init__(self, width=1, height=1, position=(0, 0), alignment=(0.5, 0.5)):
        super().__init__()
        x, y = position
        a, b = alignment
        P0 = [x + -a * width / 2, y + -b * height / 2, 0]
        P1 = [x + (1 - a) * width / 2, y + -b * height / 2, 0]
        P2 = [x + -a * width / 2, y + (1 - b) * height / 2, 0]
        P3 = [x + (1 - a) * width / 2, y + (1 - b) * height / 2, 0]
        C0, C1, C2, C3 = [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]

        position_data = [P0, P1, P3, P0, P3, P2]
        color_data = [C0, C1, C3, C0, C3, C2]

        self.add_attribute(DataType.vec3, "vertexPosition", position_data)
        self.add_attribute(DataType.vec3, "vertexColor", color_data)

        T0, T1, T2, T3 = [0, 0], [1, 0], [0, 1], [1, 1]
        uv_data = [T0, T1, T3, T0, T3, T2]
        self.add_attribute(DataType.vec2, "vertexUV", uv_data)

        normal_vector = [0, 0, 1]
        normal_data = [normal_vector] * 6
        self.add_attribute(DataType.vec3, "vertexNormal", normal_data)
        self.add_attribute(DataType.vec3, "faceNormal", normal_data)

        self.count_vertices()
