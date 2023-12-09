from core.data_type import DataType
from core.openGL_utils import OpenGLUtils
from core.uniform import Uniform
from OpenGL.GL import *


class Material:
    def __init__(self, vertex_shader_code: str, fragment_shader_code: str):

        self.program_ref = OpenGLUtils.initialize_program(
            vertex_shader_code, fragment_shader_code)
        self.uniforms = {"modelMatrix": Uniform(DataType.mat4, None),
                         "viewMatrix": Uniform(DataType.mat4, None),
                         "projectionMatrix": Uniform(DataType.mat4, None)}

        self.settings = {"drawStyle": GL_TRIANGLES}

    def add_uniform(self, data_type: DataType, variable_name: str, data):
        self.uniforms[variable_name] = Uniform(data_type, data)

    def locate_uniforms(self):
        for variable_name, uniform_object in self.uniforms.items():
            uniform_object.locate_variable(self.program_ref, variable_name)

    def update_render_settings(self):
        pass

    def set_properties(self, properties: dict):
        for name, data in properties.items():
            if name in self.uniforms.keys():
                self.uniforms[name].data = data
            elif name in self.settings.keys():
                self.settings[name] = data
            else:
                raise Exception(f"Material has no property: {name}")
