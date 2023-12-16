from OpenGL.GL import *

from core.base import Base
from core.openGL_utils import OpenGLUtils
from core.attribute import Attribute
from core.data_type import DataType


class Test(Base):
    def initialize(self):
        print("Initializing program...")
        vs_code = """
        in vec3 position;
        void main()
        {
            gl_Position = vec4(position.x, position.y, position.z, 1.0);
        }
        """
        fs_code = """
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """

        self.program_ref = OpenGLUtils.initialize_program(vs_code, fs_code)
        glLineWidth(4)

        self.vao_tri = glGenVertexArrays(1)
        glBindVertexArray(self.vao_tri)

        position_data_tri = [[-0.5, 0.8, 0.0],
                             [-0.2, 0.2, 0.0], [-0.8, 0.2, 0.0]]

        self.vertex_count_tri = len(position_data_tri)
        position_attribute_tri = Attribute(DataType.vec3, position_data_tri)
        position_attribute_tri.associate_variable(self.program_ref, "position")

        self.vao_square = glGenVertexArrays(1)
        glBindVertexArray(self.vao_square)

        position_data_square = [[0.8, 0.8, 0.0], [
            0.8, 0.2, 0.0], [0.2, 0.2, 0.0], [0.2, 0.8, 0.0]]

        self.vertex_count_square = len(position_data_square)
        position_attribute_square = Attribute(
            DataType.vec3, position_data_square)
        position_attribute_square.associate_variable(
            self.program_ref, "position")

    def update(self):
        glUseProgram(self.program_ref)
        glBindVertexArray(self.vao_tri)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertex_count_tri)

        glBindVertexArray(self.vao_square)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertex_count_square)


if __name__ == "__main__":
    Test().run()
