from material.basic_material import BasicMaterial
from OpenGL.GL import *

from material.line_type import LineType


class LineMaterial(BasicMaterial):
    def __init__(self, properties=None):
        if properties is None:
            properties = {}

        super().__init__()

        self.settings["drawStyle"] = GL_LINE_STRIP
        self.settings["lineWidth"] = 1
        self.settings["lineType"] = LineType.connected

        self.set_properties(properties)

    def update_render_settings(self):
        glLineWidth(self.settings["lineWidth"])
        self.settings["drawStyle"] = self.settings["LineType"]
