from material.basic_material import BasicMaterial
from OpenGL.GL import *


class SurfaceMaterial(BasicMaterial):
    def __init__(self, properties=None):
        if properties is None:
            properties = {}
        super().__init__()
        self.settings["drawStyle"] = GL_TRIANGLES
        self.settings["doubleSide"] = False
        self.settings["wireframe"] = False
        self.settings["lineWidth"] = 1

        self.set_properties(properties)

    def update_render_settings(self):
        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        if self.settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glLineWidth(self.settings["lineWidth"])
