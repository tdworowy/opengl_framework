from core.base import Base
from core.data_type import DataType
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.geometry import Geometry
from material.surface_material import SurfaceMaterial


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.camera.set_position([0, 0, 4])

        geometry = Geometry()
        p0 = [-0.1, 0.1, 0.0]
        p1 = [0.0, 0.0, 0.0]
        p2 = [0.1, 0.1, 0.0]
        p3 = [-0.2, -0.2, 0.0]
        p4 = [0.2, -0.2, 0.0]
        pos_data = [p0, p3, p1, p1, p3, p4, p1, p4, p2]

        r = [1, 0, 0]
        y = [1, 1, 0]
        g = [1, 0.25, 0]
        col_data = [r, g, y, y, g, g, y, g, r]

        geometry.add_attribute(DataType.vec3, "vertexPosition", pos_data)
        geometry.add_attribute(DataType.vec3, "vertexColor", col_data)
        geometry.count_vertices()

        material = SurfaceMaterial(
            {"useVertexColors": True, "wireframe": True, "lineWidth": 8})
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
