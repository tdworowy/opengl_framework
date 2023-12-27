import math

from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from effects.additive_blend_effect import AdditiveBlendEffect
from effects.bright_filter_effect import BrightFilterEffect
from effects.horizontal_blur_effect import HorizontalBlurEffect
from effects.vertical_blur_effect import VerticalBlurEffect
from geometry.rectangle_geometry import RectangleGeometry
from geometry.sphere_geometry import SphereGeometry
from extras.movement_rig import MovementRig
from core.texture import Texture
from material.texture_material import TextureMaterial
from extras.postprocessor import Postprocessor


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
        grass_material = TextureMaterial(
            Texture("../images/grass.jpg"),
            properties={
                "repeatUV": [
                    50,
                    50]})
        grass = Mesh(grass_geometry, grass_material)
        grass.rotate_x(-math.pi / 2)
        self.scene.add(grass)

        sphere_geometry = SphereGeometry()
        sphere_material = TextureMaterial(Texture("../images/grid.jpg"))
        self.sphere = Mesh(sphere_geometry, sphere_material)
        self.sphere.set_position([0, 1, 0])
        self.scene.add(self.sphere)

        self.postprocessor1 = Postprocessor(
            self.renderer, self.scene, self.camera)
        self.postprocessor1.add_effect(BrightFilterEffect(2.4))
        self.postprocessor1.add_effect(
            HorizontalBlurEffect(
                texture_size=(
                    800, 600), blur_radius=50))
        self.postprocessor1.add_effect(
            VerticalBlurEffect(
                texture_size=(
                    800, 600), blur_radius=50))

        self.postprocessor2 = Postprocessor(
            self.renderer, self.scene, self.camera)
        main_scene = self.postprocessor1.render_target_list[0].texture
        self.postprocessor2.add_effect(
            AdditiveBlendEffect(
                main_scene,
                original_strength=2,
                blend_strength=1))

    def update(self):
        self.sphere.rotate_y(0.01337)
        self.rig.update(self.input, self.delta_time)
        self.postprocessor1.render()
        self.postprocessor2.render()


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
    # TODO something is wrong with it
