from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.rectangle_geometry import RectangleGeometry
from extras.text_texture import TextTexture
from material.texture_material import TextureMaterial


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.camera.set_position([0, 0, 1.5])

        geometry = RectangleGeometry()
        message = TextTexture(
            text="Python Graphics",
            font_size=32,
            font_color=[
                0,
                0,
                200],
            image_width=256,
            image_height=256,
            align_horizontal=0.5,
            align_vertical=0.5,
            image_border_width=4,
            image_border_color=[
                255,
                0,
                0])

        material = TextureMaterial(message)
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.mesh.rotate_y(0.0114)
        self.mesh.rotate_x(0.0237)
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
