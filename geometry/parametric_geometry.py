from core.data_type import DataType
from geometry.geometry import Geometry


class ParametricGeometry(Geometry):

    def __init__(self, u_start: float, u_end: float, u_resolution: int, v_start: float,
                 v_end: float, v_resolution: int, surface_function: callable):

        super().__init__()  # super call is not in book example
        delta_u = (u_end - u_start) / u_resolution
        delta_v = (v_end - v_start) / u_resolution

        position = []

        for u_index in range(u_resolution + 1):
            v_array = []
            for v_index in range(v_resolution + 1):
                u = u_start + u_index * delta_u
                v = v_start + v_index * delta_v
                v_array.append(surface_function(u, v))
            position.append(v_array)

        position_data = []
        color_data = []

        C1, C2, C3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        C4, C5, C6 = [0, 1, 1], [1, 0, 1], [1, 1, 0]

        for x_index in range(u_resolution):
            for y_index in range(v_resolution):
                p_a = position[x_index + 0][y_index + 0]
                p_b = position[x_index + 1][y_index + 0]
                p_d = position[x_index + 0][y_index + 1]
                p_c = position[x_index + 1][y_index + 1]
                position_data += [p_a.copy(),
                                  p_b.copy(),
                                  p_c.copy(),
                                  p_a.copy(),
                                  p_c.copy(),
                                  p_d.copy()]

                color_data += [C1, C2, C3, C4, C5, C6]
        self.add_attribute(DataType.vec3, "vertexPosition", position_data)
        self.add_attribute(DataType.vec3, "vertexColor", color_data)

        self.count_vertices()
