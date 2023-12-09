from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.box_geometry import BoxGeometry
from material.surface_material import SurfaceMaterial


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderere = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.camera.set_position([0, 0, 4])

        geometry = BoxGeometry()
        material = SurfaceMaterial({"useVertexColors": True})
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.mesh.rotate_y(0.0514)
        self.mesh.rotate_x(0.0337)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
