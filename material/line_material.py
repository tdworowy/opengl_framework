from material.basic_material import BasicMaterial
from OpenGL import GL

from material.line_type import LineType


class LineMaterial(BasicMaterial):
    def __init__(self, properties=None):
        if properties is None:
            properties = {}

        super().__init__()

        self.settings["drawStyle"] = GL.GL_LINE_STRIP
        self.settings["lineWidth"] = 1
        self.settings["lineType"] = LineType.connected

        self.draw_style_map = {
            LineType.loop: GL.GL_LINE_LOOP,
            LineType.segments: GL.GL_LINES,
            LineType.connected: GL.GL_LINE_STRIP
        }

        self.set_properties(properties)

    def update_render_settings(self):
        GL.glLineWidth(self.settings["lineWidth"])
        self.settings["drawStyle"] = self.draw_style_map[self.settings["lineType"]]
