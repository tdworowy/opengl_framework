from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from geometry.sphere_geometry import SphereGeometry
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight
from light.point_light import PointLight
from material.flat_material import FlatMaterial
from material.lambert_material import LambertMaterial
from material.phong_material import PhongMaterial
from extras.directional_light_helper import DirectionalLightHelper
from extras.point_light_helper import PointLightHelper
from math import sin


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.camera.set_position([0, 0, 6])

        ambient = AmbientLight(color=(0.1, 0.1, 0.1))
        self.scene.add(ambient)

        self.directional = DirectionalLight(
            color=(0.8, 0.8, 0.8), direction=(-1, -1, -2))
        self.scene.add(self.directional)

        self.point = PointLight(color=(0.9, 0, 0), position=(1, 1, 0.8))
        self.scene.add(self.point)

        direct_helper = DirectionalLightHelper(self.directional)
        self.directional.set_direction((3, 2, 0))
        self.directional.add(direct_helper)

        point_helper = PointLightHelper(self.point)
        self.point.add(point_helper)

        sphere_geometry = SphereGeometry()
        flat_material = FlatMaterial(
            properties={
                "baseColor": [0.6, 0.2, 0, 2]})

        grid = Texture("../images/grid.jpg")

        lambert_material = LambertMaterial(texture=grid)
        phong_material = PhongMaterial(properties={"baseColor": [0.5, 0.5, 1]})

        sphere1 = Mesh(sphere_geometry, flat_material)
        sphere1.set_position([-2.2, 0, 0])
        self.scene.add(sphere1)

        sphere2 = Mesh(sphere_geometry, lambert_material)
        sphere2.set_position([0, 0, 0])
        self.scene.add(sphere2)

        sphere3 = Mesh(sphere_geometry, phong_material)
        sphere3.set_position([2.2, 0, 0])
        self.scene.add(sphere3)

    def update(self):
        self.directional.set_direction((-1, sin(0.7 * self.time), -2))
        self.point.set_position([1, sin(self.time), 0.8])
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
