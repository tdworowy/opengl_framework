from core.data_type import DataType
from geometry.geometry import Geometry


class BoxGeometry(Geometry):

    def __init__(self, width=1, height=1, depth=1):
        super().__init__()
        P0 = [-width / 2, -height / 2, -depth / 2]
        P1 = [width / 2, -height / 2, -depth / 2]
        P2 = [-width / 2, height / 2, -depth / 2]
        P3 = [width / 2, height / 2, -depth / 2]
        P4 = [-width / 2, -height / 2, depth / 2]
        P5 = [width / 2, -height / 2, depth / 2]
        P6 = [-width / 2, height / 2, depth / 2]
        P7 = [width / 2, height / 2, depth / 2]

        C1, C2 = [1, 0.5, 0.5], [0.5, 0, 0]
        C3, C4 = [0.5, 1, 0.5], [0, 0.5, 0]
        C5, C6 = [0.5, 0.5, 1], [0, 0, 0.5]

        position_data = [
            P5,
            P1,
            P3,
            P5,
            P3,
            P7,
            P0,
            P4,
            P6,
            P0,
            P6,
            P2,
            P6,
            P7,
            P3,
            P6,
            P3,
            P2,
            P0,
            P1,
            P5,
            P0,
            P5,
            P4,
            P4,
            P5,
            P7,
            P4,
            P7,
            P6,
            P1,
            P0,
            P2,
            P1,
            P2,
            P3,
        ]
        color_data = [C1] * 6 + [C2] * 6 + [C3] * 6 + [C4] * 6 + [C5] * 6 + [C6] * 6

        self.add_attribute(DataType.vec3, "vertexPosition", position_data)
        self.add_attribute(DataType.vec3, "vertexColor", color_data)

        T0, T1, T2, T3 = [0, 0], [1, 0], [0, 1], [1, 1]
        uv_data = [T0, T1, T3, T0, T3, T2] * 6
        self.add_attribute(DataType.vec2, "vertexUV", uv_data)

        N1, N2 = [1, 0, 0], [-1, 0, 0]
        N3, N4 = [0, 1, 0], [0, -1, 0]
        N5, N6 = [0, 0, 1], [0, 0, -1]
        normal_data = [N1] * 6 + [N2] * 6 + [N3] * 6 + [N4] * 6 + [N5] * 6 + [N6] * 6
        self.add_attribute(DataType.vec3, "vertexNormal", normal_data)
        self.add_attribute(DataType.vec3, "faceNormal", normal_data)

        self.count_vertices()
