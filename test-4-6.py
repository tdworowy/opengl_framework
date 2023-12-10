from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera

from extras.axes_helper import AxesHelper
from extras.grid_helper import GridHelper
from math import pi
from extras.movement_rig import MovementRig


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0.5, 1, 5])
        self.scene.add(self.rig)

        axes = AxesHelper(axis_length=2)
        self.scene.add(axes)

        grid = GridHelper(
            size=20, grid_color=[
                1, 1, 1], center_color=[
                1, 1, 0])
        grid.rotate_x(-pi / 2)
        self.scene.add(grid)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
