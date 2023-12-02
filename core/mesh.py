from core.object3D import Object3D
from OpenGL.GL import *


class Mesh(Object3D):

    def __init__(self, geometry, material):
        super().__init__()
        self.geometry = geometry
        self.material = material

        self.visible = True

        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)
        for variable_name, attribute_object in geometry.attributes.items():
            attribute_object.associate_variable(
                material.program_ref, variable_name)
        glBindVertexArray(0)
