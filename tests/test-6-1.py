from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.box_geometry import BoxGeometry
from material.surface_material import SurfaceMaterial
from core.texture import Texture
from material.texture_material import TextureMaterial
from geometry.sphere_geometry import SphereGeometry
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight
from light.point_light import PointLight
from material.flat_material import FlatMaterial
from material.lambert_material import LambertMaterial
from material.phong_material import PhongMaterial


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.camera.set_position([0, 0, 6])

        ambient = AmbientLight(color=(0.1, 0.1, 0.1))
        self.scene.add(ambient)

        directional = DirectionalLight(
            color=(0.8, 0.8, 0.8), direction=(-1, -1, -2))
        self.scene.add(directional)

        point = PointLight(color=(0.9, 0, 0), position=(1, 1, 0.8))
        self.scene.add(point)

        sphere_geometry = SphereGeometry()
        flat_material = FlatMaterial(
            properties={
                "baseColor": [
                    0.6, 0.2, 0, 2]})

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
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
    # TODO something is wrong with it
