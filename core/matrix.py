import numpy as np
from math import sin, cos, tan, pi


class Matrix:

    @staticmethod
    def make_identity() -> np.ndarray:
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]
                         ]).astype(float)

    @staticmethod
    def make_translation(x: float, y: float, z: float) -> np.ndarray:
        return np.array([[1, 0, 0, x],
                         [0, 1, 0, y],
                         [0, 0, 1, z],
                         [0, 0, 0, 1]
                         ]).astype(float)

    @staticmethod
    def make_rotation_x(angle: float) -> np.ndarray:
        c = cos(angle)
        s = sin(angle)
        return np.array([[1, 0, 0, 0],
                         [0, c, -s, 0],
                         [0, s, c, 0],
                         [0, 0, 0, 1]
                         ]).astype(float)

    @staticmethod
    def make_rotation_y(angle: float) -> np.ndarray:
        c = cos(angle)
        s = sin(angle)
        return np.array([[c, 0, s, 0],
                         [0, 1, 0, 0],
                         [-s, 0, c, 0],
                         [0, 0, 0, 1]
                         ]).astype(float)

    @staticmethod
    def make_rotation_z(angle: float) -> np.ndarray:
        c = cos(angle)
        s = sin(angle)
        return np.array([[c, -s, 0, 0],
                         [s, c, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]
                         ]).astype(float)

    @staticmethod
    def make_scale(s: float) -> np.ndarray:
        return np.array([[s, 0, 0, 0],
                         [0, s, 0, 0],
                         [0, 0, s, 0],
                         [0, 0, 0, 1]
                         ]).astype(float)

    @staticmethod
    def make_perspective(angle_of_view=60, aspect_ratio=1,
                         near=0.1, far=1000) -> np.ndarray:
        a = angle_of_view * pi / 180.0
        d = 1.0 / tan(a / 2)
        r = aspect_ratio
        b = (far + near) / (near - far)
        c = 2 * far * near / (near - far)
        return np.array([[d / r, 0, 0, 0],
                         [0, d, 0, 0],
                         [0, 0, b, c],
                         [0, 0, -1, 0]
                         ]).astype(float)