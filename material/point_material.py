from material.basic_material import BasicMaterial
from OpenGL import GL


class PointMaterial(BasicMaterial):
    def __init__(self, properties=None):
        if properties is None:
            properties = {}
        super().__init__()

        self.settings["drawStyle"] = GL.GL_POINTS
        self.settings["pointSize"] = 8
        self.settings["roundedPoints"] = False

        self.set_properties(properties)

    def update_render_settings(self):
        GL.glPointSize(self.settings["pointSize"])
        if self.settings["roundedPoints"]:
            GL.glEnable(GL.GL_POINT_SMOOTH)
        else:
            GL.glDisable(GL.GL_POINT_SMOOTH)
