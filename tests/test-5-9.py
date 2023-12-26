from math import floor

from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from extras.grid_helper import GridHelper
from extras.movement_rig import MovementRig
from geometry.rectangle_geometry import RectangleGeometry
from material.spite_material import SpriteMaterial
from core.texture import Texture


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 0.5, 3])

        self.scene.add(self.rig)

        geometry = RectangleGeometry()
        tile_set = Texture("../images/crate.jpg")
        spriteMaterial = SpriteMaterial(tile_set, {
            "billboard": 1,
            "tileCount": [4, 4],
            "tileNumber": 0
        })
        self.tiles_per_second = 8

        self.sprite = Mesh(geometry, spriteMaterial)
        self.scene.add(self.sprite)

        grid = GridHelper()
        grid.rotate_x(-3.14 / 2)
        self.scene.add(grid)

    def update(self):
        tile_number = floor(self.time * self.tiles_per_second)
        self.sprite.material.uniforms["tileNumber"].data = tile_number
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
