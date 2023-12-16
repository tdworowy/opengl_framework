from core.base import Base
from core.openGL_utils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *
from core.data_type import DataType


class Test(Base):
    def initialize(self):
        print("Initializing program...")
        vs_code = """
        in vec3 position;
        in vec3 vertexColor;
        out vec3 color;
        void main()
        {
            gl_Position = vec4(position.x, position.y, position.z, 1.0);
            color = vertexColor;
        }
        """
        fs_code = """
        in vec3 color;
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(color.r, color.g, color.b, 1.0);
        }
        """

        self.program_ref = OpenGLUtils.initialize_program(vs_code, fs_code)
        glPointSize(10)
        glLineWidth(4)

        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)

        position_data = [[0.8, 0.0, 0.0], [0.4, 0.6, 0.0], [-0.4, 0.6, 0.0], [-0.8, 0.0, 0.0], [-0.4, -0.6, 0.0],
                         [0.4, -0.6, 0.0]]

        self.vertex_count = len(position_data)
        position_attribute = Attribute(DataType.vec3, position_data)
        position_attribute.associate_variable(self.program_ref, "position")

        color_data = [[1.0, 0.0, 0.0], [1.0, 0.5, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
                      [0.5, 0.0, 1.0]]

        color_attribute = Attribute(DataType.vec3, color_data)
        color_attribute.associate_variable(self.program_ref, "vertexColor")

    def update(self):
        glUseProgram(self.program_ref)
        glDrawArrays(GL_POINTS, 0, self.vertex_count)


if __name__ == "__main__":
    Test().run()
