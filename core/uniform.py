from OpenGL.GL import *

from core.data_type import DataType


class Uniform:
    def __init__(self, data_type: DataType, data):
        self.data_type = data_type
        self.data = data

        self.variable_ref = None

    def locate_variable(self, program_ref, variable_name: str):
        self.variable_ref = glGetUniformLocation(program_ref, variable_name)

    def upload_data(self):
        if self.variable_ref == -1:
            return
        match self.data_type:
            case DataType.int:
                glUniform1i(self.variable_ref, self.data)
            case DataType.bool:
                glUniform1i(self.variable_ref, self.data)
            case DataType.float:
                glUniform1f(self.variable_ref, self.data)
            case DataType.vec2:
                glUniform2f(self.variable_ref, self.data[0], self.data[1])
            case DataType.vec3:
                glUniform3f(
                    self.variable_ref,
                    self.data[0],
                    self.data[1],
                    self.data[2])
            case DataType.vec4:
                glUniform4f(
                    self.variable_ref,
                    self.data[0],
                    self.data[1],
                    self.data[2],
                    self.data[3])
            case _:
                raise Exception(
                    f"Unknown type {self.data_type}")
