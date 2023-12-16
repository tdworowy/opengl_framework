from core.base import Base
from core.data_type import DataType
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.geometry import Geometry
from math import sin
from numpy import arange
from material.point_material import PointMaterial
from material.line_material import LineMaterial


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.camera.set_position([0, 0, 4])

        geometry = Geometry()
        pos_data = []
        for x in arange(-3.2, 3.2, 0.3):
            pos_data.append([x, sin(x), 0])
        geometry.add_attribute(DataType.vec3, "vertexPosition", pos_data)
        geometry.count_vertices()

        point_material = PointMaterial(
            {"baseColor": [1, 1, 0], "pointSize": 10})
        point_mesh = Mesh(geometry, point_material)

        line_material = LineMaterial({"baseColor": [1, 0, 1], "lineWidth": 4})
        line_mesh = Mesh(geometry, line_material)

        self.scene.add(point_mesh)
        self.scene.add(line_mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
