import numpy as np
from core.matrix import Matrix


class Object3D:
    def __init__(self):
        self.transform = Matrix.make_identity()
        self.parent = None
        self.children = []

    def add(self, child):
        self.children.append(child)
        child.parent = self

    def remove(self, child):
        self.children.remove(child)
        child.parent = None

    def get_world_matrix(self):
        if self.parent is None:
            return self.transform
        else:
            return self.parent.get_world_matrix() @ self.transform

    def get_descendant_list(self) -> list:
        descendant = []
        node_to_process = [self]

        while len(node_to_process) > 0:
            node = node_to_process.pop(0)
            descendant.append(node)
            node_to_process = node.children + node_to_process

        return descendant

    def apply_matrix(self, matrix: np.ndarray, local_coord=True):
        if local_coord:
            self.transform = self.transform @ matrix
        else:
            self.transform = matrix @ self.transform

    def translate(self, x: int, y: int, z: int, local_coord=True):
        m = Matrix.make_translation(x, y, z)
        self.apply_matrix(m, local_coord)

    def rotate_x(self, angle: float, local_coord=True):
        m = Matrix.make_rotation_x(angle)
        self.apply_matrix(m, local_coord)

    def rotate_y(self, angle: float, local_coord=True):
        m = Matrix.make_rotation_y(angle)
        self.apply_matrix(m, local_coord)

    def rotate_z(self, angle: float, local_coord=True):
        m = Matrix.make_rotation_z(angle)
        self.apply_matrix(m, local_coord)

    def scale(self, s: int, local_coord=True):
        m = Matrix.make_scale(s)
        self.apply_matrix(m, local_coord)

    def get_position(self) -> list[int]:
        return [
            self.transform.item((0, 3)),
            self.transform.item((1, 3)),
            self.transform.item((2, 3)),
        ]

    def get_world_position(self) -> list[int]:
        world_transform = self.get_world_matrix()
        return [
            world_transform.item((0, 3)),
            world_transform.item((1, 3)),
            world_transform.item((2, 3)),
        ]

    def set_position(self, position: list[int]):
        self.transform.itemset((0, 3), position[0])
        self.transform.itemset((1, 3), position[1])
        self.transform.itemset((2, 3), position[2])

    def look_at(self, target_position: list[int]):
        self.transform = Matrix.make_look_at(self.get_world_position(), target_position)

    def get_rotation_matrix(self) -> np.ndarray:
        return np.array(
            [self.transform[0][0:3], self.transform[1][0:3], self.transform[2][0:3]]
        )

    def get_direction(self) -> list[int]:
        forward = np.array([0, 0, -1])
        return list(self.get_rotation_matrix() @ forward)

    def set_direction(self, direction: tuple):
        position = self.get_position()
        target_position = [
            position[0] + direction[0],
            position[1] + direction[1],
            position[2] + direction[2],
        ]
        self.look_at(target_position)
