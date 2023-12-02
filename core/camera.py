from core.object3D import Object3D
from core.matrix import Matrix
from numpy.linalg import inv


class Camera(Object3D):
    def __init__(self, angle_of_view=60, aspect_ratio=1, near=0.1, far=1000):
        super().__init__()
        self.projection_matrix = Matrix.make_perspective(
            angle_of_view, aspect_ratio, near, far)
        self.view_matrix = Matrix.make_identity()

    def update_view_matrix(self):
        self.view_matrix = inv(self.get_world_matrix())
