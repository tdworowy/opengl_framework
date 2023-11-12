from OpenGL.GL import *

from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from core.data_type import DataType


class Test(Base):

    def initialize(self):
        print("initializing program...")

        vs_code = """
        in vec3 position;
        uniform vec3 translation;
        void main()
        {
            vec3 pos = position + translation;
            gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
        }
        """
        fs_code = """
        uniform vec3 baseColor;
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
        }
        """

        self.program_ref = OpenGLUtils.initialize_program(vs_code, fs_code)
        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        position_data = [[0.0, 0.2, 0.0], [0.2, -0.2, 0.0], [-0.2, -0.2, 0.0]]
        self.vertex_count = len(position_data)
        position_attribute = Attribute(DataType.vec3, position_data)
        position_attribute.associate_variable(self.program_ref, "position")

        self.translation1 = Uniform(DataType.vec3, [-0.5, 0.0, 0.0])
        self.translation1.locate_variable(self.program_ref, "translation")

        self.translation2 = Uniform(DataType.vec3, [0.5, 0.0, 0.0])
        self.translation2.locate_variable(self.program_ref, "translation")

        self.base_color1 = Uniform(DataType.vec3, [1.0, 0.0, 0.0])
        self.base_color1.locate_variable(self.program_ref, "baseColor")

        self.base_color2 = Uniform(DataType.vec3, [0.0, 0.0, 1.0])
        self.base_color2.locate_variable(self.program_ref, "baseColor")

    def update(self):
        glUseProgram(self.program_ref)

        self.translation1.upload_data()
        self.base_color1.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

        self.translation2.upload_data()
        self.base_color2.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)


if __name__ == "__main__":
    Test().run()
