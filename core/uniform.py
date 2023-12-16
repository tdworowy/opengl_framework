from OpenGL import GL

from core.data_type import DataType


class Uniform:
    def __init__(self, data_type: DataType, data):
        self.data_type = data_type
        self.data = data

        self.variable_ref = None

    def locate_variable(self, program_ref, variable_name: str):
        self.variable_ref = GL.glGetUniformLocation(program_ref, variable_name)

    def upload_data(self):
        if self.variable_ref == -1:
            return
        match self.data_type:
            case DataType.int:
                GL.glUniform1i(self.variable_ref, self.data)
            case DataType.bool:
                GL.glUniform1i(self.variable_ref, self.data)
            case DataType.float:
                GL.glUniform1f(self.variable_ref, self.data)
            case DataType.vec2:
                GL.glUniform2f(self.variable_ref, self.data[0], self.data[1])
            case DataType.vec3:
                GL.glUniform3f(
                    self.variable_ref,
                    self.data[0],
                    self.data[1],
                    self.data[2])
            case DataType.vec4:
                GL.glUniform4f(
                    self.variable_ref,
                    self.data[0],
                    self.data[1],
                    self.data[2],
                    self.data[3])
            case DataType.mat4:
                GL.glUniformMatrix4fv(
                    self.variable_ref, 1, GL.GL_TRUE, self.data)
            case DataType.sampler2D:
                texture_object_ref, texture_unit_ref = self.data
                GL.glActiveTexture(GL.GL_TEXTURE0 + texture_unit_ref)
                GL.glBindTexture(GL.GL_TEXTURE_2D, texture_object_ref)
                GL.glUniform1i(self.variable_ref, texture_unit_ref)
            case _:
                raise Exception(
                    f"Unknown type {self.data_type}")
