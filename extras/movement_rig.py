from math import pi

from core.input import Input
from core.object3D import Object3D


class MovementRig(Object3D):
    def __init__(self, unit_per_second=1, degrees_per_second=60):
        super().__init__()
        self.look_attachment = Object3D()
        self.children = [self.look_attachment]
        self.look_attachment.parent = self

        self.unit_per_second = unit_per_second
        self.degrees_per_second = degrees_per_second

        self.KEY_MOVE_FORWARDS = "w"
        self.KEY_MOVE_BACKWARDS = "s"
        self.KEY_MOVE_LEFT = "a"
        self.KEY_MOVE_RIGHT = "d"
        self.KEY_MOVE_UP = "r"
        self.KEY_MOVE_DOWN = "f"
        self.KEY_TURN_LEFT = "q"
        self.KEY_TURN_RIGHT = "e"
        self.KEY_LOOK_UP = "t"
        self.KEY_LOOK_DOWN = "g"

    def add(self, child: Object3D):
        self.look_attachment.add(child)

    def remove(self, child: Object3D):
        self.look_attachment.remove(child)

    def update(self, input_object: Input, delta_time: int):
        move_amount = self.unit_per_second * delta_time
        rotate_amount = self.degrees_per_second * (pi / 180) * delta_time
        if input_object.is_key_pressed(self.KEY_MOVE_FORWARDS):
            self.translate(0, 0, -move_amount)
        if input_object.is_key_pressed(self.KEY_MOVE_BACKWARDS):
            self.translate(0, 0, move_amount)
        if input_object.is_key_pressed(self.KEY_MOVE_LEFT):
            self.translate(-move_amount, 0, 0)
        if input_object.is_key_pressed(self.KEY_MOVE_RIGHT):
            self.translate(move_amount, 0, 0)
        if input_object.is_key_pressed(self.KEY_MOVE_UP):
            self.translate(0, move_amount, 0)
        if input_object.is_key_pressed(self.KEY_MOVE_DOWN):
            self.translate(0, -move_amount, 0)
        if input_object.is_key_pressed(self.KEY_TURN_RIGHT):
            self.rotate_y(-rotate_amount)
        if input_object.is_key_pressed(self.KEY_TURN_LEFT):
            self.rotate_y(rotate_amount)
        if input_object.is_key_pressed(self.KEY_LOOK_UP):
            self.look_attachment.rotate_x(rotate_amount)
        if input_object.is_key_pressed(self.KEY_LOOK_DOWN):
            self.look_attachment.rotate_x(-rotate_amount)
