from core.data_type import DataType
from geometry.geometry import Geometry


class RectangleGeometry(Geometry):

    def __init__(self, width=1, height=1):
        super().__init__()
        P0 = [-width / 2, -height / 2, 0]
        P1 = [width / 2, -height / 2, 0]
        P2 = [-width / 2, height / 2, 0]
        P3 = [width / 2, height / 2, 0]
        C0, C1, C2, C3 = [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]

        position_data = [P0, P1, P3, P0, P3, P2]
        color_data = [C0, C1, C3, C0, C3, C2]

        self.add_attribute(DataType.vec3, "vertexPosition", position_data)
        self.add_attribute(DataType.vec3, "vertexColor", color_data)

        self.count_vertices()
