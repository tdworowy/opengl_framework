from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight
from material.phong_material import PhongMaterial
from geometry.rectangle_geometry import RectangleGeometry
from geometry.sphere_geometry import SphereGeometry
from extras.movement_rig import MovementRig
from extras.directional_light_helper import DirectionalLightHelper
from material.texture_material import TextureMaterial


class Test(Base):
    def initialize(self):
        self.renderer = Renderer((0.2, 0.2, 0.2))
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 2, 5])

        amb_light = AmbientLight(color=(0.2, 0.2, 0.2))
        self.scene.add(amb_light)

        self.dir_light = DirectionalLight(direction=(-1, -1, 0))
        self.dir_light.set_position([2, 4, 0])
        direct_helper = DirectionalLightHelper(self.dir_light)
        self.dir_light.add(direct_helper)
        self.scene.add(self.dir_light)

        sphere_geometry = SphereGeometry()
        phong_material = PhongMaterial(
            Texture("../images/grid.jpg"), use_shadow=True)

        sphere1 = Mesh(sphere_geometry, phong_material)
        sphere1.set_position([-2, 1, 0])
        self.scene.add(sphere1)

        sphere2 = Mesh(sphere_geometry, phong_material)
        sphere2.set_position([1, 2.2, -0.5])
        self.scene.add(sphere2)

        self.renderer.enable_shadows(self.dir_light)

        depth_texture = self.renderer.shadow_object.render_target.texture
        shadow_display = Mesh(
            RectangleGeometry(),
            TextureMaterial(depth_texture))
        shadow_display.set_position([-1, 3, 0])
        self.scene.add(shadow_display)

        floor = Mesh(RectangleGeometry(width=20, height=20), phong_material)
        floor.rotate_x(-3.14 / 2)
        self.scene.add(floor)

    def update(self):
        self.dir_light.rotate_y(0.01337, False)
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)

        shadow_cam = self.renderer.shadow_object.camera
        self.renderer.render(self.scene, shadow_cam)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
    # TODO something is wrong with it
