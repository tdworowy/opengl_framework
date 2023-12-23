from core.data_type import DataType
from material.material import Material


class BaseEffect(Material):

    def __init__(self, vertex_shader_code: str, fragment_shader_code: str):
        super().__init__(vertex_shader_code, fragment_shader_code)
