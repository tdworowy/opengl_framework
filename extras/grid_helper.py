from core.data_type import DataType
from core.mesh import Mesh
from geometry.geometry import Geometry
from material.line_material import LineMaterial
from material.line_type import LineType


class GridHelper(Mesh):
    def __init__(
        self,
        size=10,
        divisions=10,
        grid_color=(0, 0, 0),
        center_color=(0.5, 0.5, 0.5),
        line_width=1,
    ):
        geometry = Geometry()
        position_data = []
        color_data = []
        values = []
        delta_size = size / divisions

        for n in range(divisions + 1):
            values.append(-size / 2 + n * delta_size)

        for x in values:
            position_data.append([x, -size / 2, 0])
            position_data.append([x, size / 2, 0])
            if x == 0:
                color_data.append(center_color)
                color_data.append(center_color)
            else:
                color_data.append(grid_color)
                color_data.append(grid_color)

        for y in values:
            position_data.append([-size / 2, y, 0])
            position_data.append([size / 2, y, 0])
            if y == 0:
                color_data.append(center_color)
                color_data.append(center_color)
            else:
                color_data.append(grid_color)
                color_data.append(grid_color)

        geometry.add_attribute(DataType.vec3, "vertexPosition", position_data)
        geometry.add_attribute(DataType.vec3, "vertexColor", color_data)
        geometry.count_vertices()

        material = LineMaterial(
            {
                "useVertexColors": True,
                "lineWidth": line_width,
                "lineType": LineType.segments,
            }
        )

        super().__init__(geometry, material)
