from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.rectangle_geometry import RectangleGeometry
from geometry.sphere_geometry import SphereGeometry
from extras.movement_rig import MovementRig
from core.texture import Texture
from material.texture_material import TextureMaterial


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.set_position([0, 1, 4])

        sky_geometry = SphereGeometry(radius=50)
        sky_material = TextureMaterial(Texture("../images/sky.jpg"))
        sky = Mesh(sky_geometry, sky_material)
        self.scene.add(sky)

        grass_geometry = RectangleGeometry(width=100, height=100)
        grass_material = TextureMaterial(Texture("../images/grass.jpg"))
        grass = Mesh(grass_geometry, grass_material)
        self.scene.add(grass)

    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.rig.update(self.input, self.delta_time)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
