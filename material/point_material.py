from material.basic_material import BasicMaterial
from OpenGL.GL import *


class PointMaterial(BasicMaterial):
    def __init__(self, properties=None):
        if properties is None:
            properties = {}
        super().__init__()

        self.settings["drawStyle"] = GL_POINT
        self.settings["pointSize"] = 8
        self.settings["roundedPoints"] = False

        self.set_properties(properties)

    def update_render_settings(self):
        glPointSize(self.settings["pointSize"])
        if self.settings["roundedPoints"]:
            glEnable(GL_POINT_SMOOTH)
        else:
            glDisable(GL_POINT_SMOOTH)
