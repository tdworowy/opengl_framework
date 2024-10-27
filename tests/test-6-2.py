from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.rectangle_geometry import RectangleGeometry
from light.ambient_light import AmbientLight
from light.point_light import PointLight
from material.lambert_material import LambertMaterial
from core.texture import Texture


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.camera.set_position([0, 0, 2.5])

        ambient_light = AmbientLight(color=(0.3, 0.3, 0.3))
        self.scene.add(ambient_light)

        point_light = PointLight(color=(1, 1, 1), position=(1.2, 1.2, 0.3))
        self.scene.add(point_light)

        color_tex = Texture("../images/brick-wall.jpg")
        bump_tex = Texture("../images/brick-wall-normal-map.jpg")

        geometry = RectangleGeometry(width=2, height=2)
        bump_material = LambertMaterial(
            texture=color_tex, bump_texture=bump_tex, properties={"bumpStrength": 1}
        )

        mesh = Mesh(geometry, bump_material)
        self.scene.add(mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
