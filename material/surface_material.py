from material.basic_material import BasicMaterial
from OpenGL import GL


class SurfaceMaterial(BasicMaterial):
    def __init__(self, properties=None):
        if properties is None:
            properties = {}
        super().__init__()
        self.settings["drawStyle"] = GL.GL_TRIANGLES
        self.settings["doubleSide"] = False
        self.settings["wireframe"] = False
        self.settings["lineWidth"] = 1

        self.set_properties(properties)

    def update_render_settings(self):
        if self.settings["doubleSide"]:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)

        if self.settings["wireframe"]:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

        GL.glLineWidth(self.settings["lineWidth"])
