import math

from core.base import Base
from core.render_target import RenderTarget
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.rectangle_geometry import RectangleGeometry
from geometry.sphere_geometry import SphereGeometry
from geometry.box_geometry import BoxGeometry
from extras.movement_rig import MovementRig
from core.texture import Texture
from material.texture_material import TextureMaterial
from material.surface_material import SurfaceMaterial


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
        grass.rotate_x(-math.pi / 2)
        self.scene.add(grass)

        sphere_geometry = SphereGeometry()
        sphere_material = TextureMaterial(Texture("../images/grid.jpg"))
        self.sphere = Mesh(sphere_geometry, sphere_material)
        self.sphere.set_position([0, 1, 0])
        self.scene.add(self.sphere)

        box_geometry = BoxGeometry(width=2, height=2, depth=0.2)
        box_material = SurfaceMaterial({"baseColor": [0, 0, 0]})
        box = Mesh(box_geometry, box_material)
        box.set_position([2, 1, 0])
        self.scene.add(box)

        self.render_target = RenderTarget(resolution=(512, 512))
        screen_geometry = RectangleGeometry(width=1.1, height=1.1)
        screen_material = TextureMaterial(self.render_target.texture)
        screen = Mesh(screen_geometry, screen_material)
        screen.set_position([1.2, 1, 0.11])
        self.scene.add(screen)

        self.sky_camera = Camera(angle_of_view=512 / 512)
        self.sky_camera.set_position([0, 10, 0.1])
        self.sky_camera.look_at([0, 0, 0])
        self.scene.add(self.sky_camera)

    def update(self):
        self.sphere.rotate_y(0.01337)
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(
            self.scene,
            self.sky_camera,
            render_target=self.render_target)
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
    # TODO something is wrong with it