from core.data_type import DataType
from geometry.geometry import Geometry
import numpy as np


def calc_normal(p0, p1, p2):
    v1 = np.array(p1) - np.array(p0)
    v2 = np.array(p2) - np.array(p0)
    orthogonal_vector = np.cross(v1, v2)
    norm = np.linalg.norm(orthogonal_vector)
    normal_vector = orthogonal_vector / norm if norm > 1e-6 \
        else np.array(p0) / np.linalg.norm(p0)
    return normal_vector


class ParametricGeometry(Geometry):

    def __init__(self, u_start: float, u_end: float, u_resolution: int, v_start: float,
                 v_end: float, v_resolution: int, surface_function: callable):

        super().__init__()  # super call is not in book example
        delta_u = (u_end - u_start) / u_resolution
        delta_v = (v_end - v_start) / v_resolution

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

        uvs = []
        uv_data = []
        for u_index in range(u_resolution + 1):
            v_array = []
            for v_index in range(v_resolution + 1):
                u = u_index / u_resolution
                v = v_index / v_resolution
                v_array.append([u, v])
            uvs.append(v_array)

        vertex_normals = []
        for u_index in range(u_resolution + 1):
            v_array = []
            for v_index in range(v_resolution + 1):
                u = u_start + u_index * delta_u
                v = v_start + v_index * delta_v
                h = 0.0001
                P0 = surface_function(u, v)
                P1 = surface_function(u + h, v)
                P2 = surface_function(u, v + h)
                normal_vector = calc_normal(P0, P1, P2)
                v_array.append(normal_vector)
            vertex_normals.append(v_array)

        vertex_normal_data = []
        face_normal_data = []
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
                uv_a = uvs[x_index + 0][y_index + 0]
                uv_b = uvs[x_index + 1][y_index + 0]
                uv_c = uvs[x_index + 0][y_index + 1]
                uv_d = uvs[x_index + 1][y_index + 1]
                uv_data += [uv_a, uv_b, uv_c,
                            uv_a, uv_c, uv_d]

                n_a = vertex_normals[x_index + 0][y_index + 0]
                n_b = vertex_normals[x_index + 1][y_index + 0]
                n_c = vertex_normals[x_index + 0][y_index + 1]
                n_d = vertex_normals[x_index + 1][y_index + 1]
                vertex_normal_data += [n_a.copy(), n_b.copy(), n_c.copy(),
                                       n_a.copy(), n_c.copy(), n_d.copy()]

                fn0 = calc_normal(p_a, p_b, p_c)
                fn1 = calc_normal(p_a, p_c, p_d)
                face_normal_data += [fn0.copy(), fn0.copy(), fn0.copy(),
                                     fn1.copy(), fn1.copy(), fn1.copy()]

        self.add_attribute(DataType.vec3, "vertexPosition", position_data)
        self.add_attribute(DataType.vec3, "vertexColor", color_data)
        self.add_attribute(DataType.vec2, "vertexUV", uv_data)
        self.add_attribute(DataType.vec3, "vertexNormal", vertex_normal_data)
        self.add_attribute(DataType.vec3, "faceNormal", face_normal_data)

        self.count_vertices()
