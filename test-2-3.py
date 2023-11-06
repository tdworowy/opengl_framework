from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute, DataType
from OpenGL.GL import *


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

        voe_ref = glGenVertexArrays(1)
        glBindVertexArray(voe_ref)

        position_data = [[0.8, 0.0, 0.0], [0.4, 0.6, 0.0], [-0.4, 0.6, 0.0], [-0.8, 0.0, 0.0], [-0.4, -0.6, 0.0],
                         [0.4, -0.6, 0.0]]

        self.vertex_count = len(position_data)
        position_attribute = Attribute(DataType.vec3, position_data)
        position_attribute.associate_variable(self.program_ref, "position")

    def update(self):
        glUseProgram(self.program_ref)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertex_count)


if __name__ == "__main__":
    Test().run()
