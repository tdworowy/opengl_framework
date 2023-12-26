from OpenGL import GL

from core.data_type import DataType


class Uniform:
    def __init__(self, data_type: DataType, data):
        self.data_type = data_type
        self.data = data

        self.variable_ref = None

    def locate_variable(self, program_ref, variable_name: str):
        match self.data_type:
            case DataType.light:
                self.variable_ref = {}
                self.variable_ref["lightType"] = GL.glGetUniformLocation(
                    program_ref, f"{variable_name}.lightType")
                self.variable_ref["color"] = GL.glGetUniformLocation(
                    program_ref, f"{variable_name}.color")
                self.variable_ref["direction"] = GL.glGetUniformLocation(
                    program_ref, f"{variable_name}.direction")
                self.variable_ref["position"] = GL.glGetUniformLocation(
                    program_ref, f"{variable_name}.position")
                self.variable_ref["attenuation"] = GL.glGetUniformLocation(
                    program_ref, f"{variable_name}.attenuation")

            case DataType.shadow:
                self.variable_ref = {}
                self.variable_ref["lightDirection"] = GL.glGetUniformLocation(
                    program_ref, f"{variable_name}.lightDirection")
                self.variable_ref["projectionMatrix"] = GL.glGetUniformLocation(program_ref,
                                                                                f"{variable_name}.projectionMatrix")
                self.variable_ref["viewMatrix"] = GL.glGetUniformLocation(program_ref,
                                                                          f"{variable_name}.viewMatrix")
                self.variable_ref["depthTextureSampler"] = GL.glGetUniformLocation(program_ref,
                                                                                   f"{variable_name}.depthTextureSampler")
                self.variable_ref["strength"] = GL.glGetUniformLocation(program_ref,
                                                                        f"{variable_name}.strength")
                self.variable_ref["bias"] = GL.glGetUniformLocation(program_ref,
                                                                    f"{variable_name}.bias")

            case _:
                self.variable_ref = GL.glGetUniformLocation(
                    program_ref, variable_name)

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
                GL.glUniform2f(self.variable_ref, *self.data)
            case DataType.vec3:
                GL.glUniform3f(
                    self.variable_ref,
                    *self.data[0:3])
            case DataType.vec4:
                GL.glUniform4f(
                    self.variable_ref,
                    *self.data
                )
            case DataType.mat4:
                GL.glUniformMatrix4fv(
                    self.variable_ref, 1, GL.GL_TRUE, self.data)
            case DataType.sampler2D:
                texture_object_ref, texture_unit_ref = self.data
                GL.glActiveTexture(GL.GL_TEXTURE0 + texture_unit_ref)
                GL.glBindTexture(GL.GL_TEXTURE_2D, texture_object_ref)
                GL.glUniform1i(self.variable_ref, texture_unit_ref)
            case DataType.light:
                GL.glUniform1i(
                    self.variable_ref["lightType"],
                    self.data.light_type)
                GL.glUniform3f(self.variable_ref["color"], *self.data.color)
                direction = self.data.get_direction()
                GL.glUniform3f(self.variable_ref["direction"], *direction)
                position = self.data.get_position()
                GL.glUniform3f(self.variable_ref["position"], *position)
                GL.glUniform3f(
                    self.variable_ref["attenuation"],
                    *self.data.attenuation)
            case DataType.shadow:
                direction = self.data.light_source.get_direction()
                GL.glUniform3f(self.variable_ref["lightDirection"], *direction)
                GL.glUniformMatrix4fv(
                    self.variable_ref["projectionMatrix"],
                    1,
                    GL.GL_TRUE,
                    self.data.camare.projection_matrix)
                GL.glUniformMatrix4fv(self.variable_ref["viewMatrix"], 1, GL.GL_TRUE,
                                      self.data.camare.view_matrix)

                texture_object_ref = self.data.render_target.texture.texture_ref
                texture_unit_ref = 15
                GL.glActiveTexture(f"{GL.GL_TEXTURE0}{texture_unit_ref}")
                GL.glBindTexture(GL.GL_TEXTURE_2D, texture_object_ref)
                GL.glUniform1i(
                    self.variable_ref["depthTextureSampler"],
                    texture_unit_ref)

                GL.glUniform1f(
                    self.variable_ref["strength"],
                    self.data.strength)
                GL.glUniform1f(self.variable_ref["bias"], self.data.bias)
            case _:
                raise Exception(
                    f"Unknown type {self.data_type}")
