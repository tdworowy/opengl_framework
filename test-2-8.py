from math import sin, cos
from OpenGL.GL import *

from core.base import Base
from core.openGL_utils import OpenGLUtils
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

        self.translation = Uniform(DataType.vec3, [-0.5, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, "translation")

        self.base_color = Uniform(DataType.vec3, [1.0, 0.0, 0.0])
        self.base_color.locate_variable(self.program_ref, "baseColor")

    def update(self):

        self.translation.data[0] = 0.75 * cos(self.time)
        self.translation.data[1] = 0.75 * sin(self.time)

        self.base_color.data[0] = (sin(self.time) + 1) / 2
        self.base_color.data[1] = (sin(self.time + 3) + 1) / 2
        self.base_color.data[2] = (sin(self.time + 5) + 1) / 2

        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(self.program_ref)

        self.translation.upload_data()
        self.base_color.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)


if __name__ == "__main__":
    Test().run()
