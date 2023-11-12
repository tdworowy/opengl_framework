from OpenGL.GL import *
import numpy as np

from core.data_type import DataType


class Attribute:
    def __init__(self, data_type: DataType, data: list[list[float]]):
        self.data_type = data_type
        self.data = data

        self.buffer_ref = glGenBuffers(1)
        self.upload_data()

    def upload_data(self):
        data = np.array(self.data).astype(np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ref)
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def associate_variable(self, program_ref: str, variable_name: str):
        variable_ref = glGetAttribLocation(program_ref, variable_name)

        if variable_ref == -1:
            return

        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ref)

        match self.data_type:
            case DataType.int:
                glVertexAttribPointer(variable_ref, 1, GL_INT, False, 0, None)
            case DataType.float:
                glVertexAttribPointer(
                    variable_ref, 1, GL_FLOAT, False, 0, None)
            case DataType.vec2:
                glVertexAttribPointer(
                    variable_ref, 2, GL_FLOAT, False, 0, None)
            case DataType.vec3:
                glVertexAttribPointer(
                    variable_ref, 3, GL_FLOAT, False, 0, None)
            case DataType.vec4:
                glVertexAttribPointer(
                    variable_ref, 4, GL_FLOAT, False, 0, None)
            case _:
                raise Exception(
                    f"Attribute {variable_name} has unknown type {self.data_type}")

        glEnableVertexAttribArray(variable_ref)
