from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.rectangle_geometry import RectangleGeometry
from geometry.box_geometry import BoxGeometry
from extras.movement_rig import MovementRig
from extras.grid_helper import GridHelper
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
        self.rig.set_position([0, 0.5, 3])
        self.scene.add(self.rig)

        crate_geometry = BoxGeometry()
        crate_material = TextureMaterial(Texture("../images/crate.jpg"))
        crate = Mesh(crate_geometry, crate_material)
        self.scene.add(crate)  # TODO for some reason create is invisible

        grid = GridHelper(grid_color=[1, 1, 1], center_color=[1, 1, 0])
        grid.rotate_x(-3.14 / 2)
        self.scene.add(grid)

        self.hud_scene = Scene()
        self.hud_camera = Camera()
        self.hud_camera.set_orthographic(0, 800, 0, 600, 1, -1)

        label_geo1 = RectangleGeometry(
            width=600, height=80, position=(0, 600), alignment=(0, 1)
        )
        label_mat1 = TextureMaterial(Texture("../images/crate.jpg"))
        label1 = Mesh(label_geo1, label_mat1)
        self.hud_scene.add(label1)

        label_geo2 = RectangleGeometry(
            width=400, height=80, position=(800, 0), alignment=(1, 0)
        )
        label_mat2 = TextureMaterial(Texture("../images/crate-simulator.png"))
        label2 = Mesh(label_geo2, label_mat2)
        self.hud_scene.add(label2)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)
        self.renderer.render(self.hud_scene, self.hud_camera, clear_color=False)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
