from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.rectangle_geometry import RectangleGeometry
from material.surface_material import SurfaceMaterial
from core.texture import Texture
from material.texture_material import TextureMaterial


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.camera.set_position([0, 0, 2])

        geometry = RectangleGeometry()
        grid = Texture("../images/grid.jpg")
        material = TextureMaterial(grid)
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
