from OpenGL.GL import *

from core.base import Base
from core.openGLUtils import OpenGLUtils


class Test(Base):

    def initialize(self):
        print("Initializing Program...")
        vs_code = """
        void main()
        {
            gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
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
        voa_ref = glGenVertexArrays(1)
        glBindVertexArray(voa_ref)

        glPointSize(10)

    def update(self):
        glUseProgram(self.program_ref)
        glDrawArrays(GL_POINTS, 0, 1)


if __name__ == "__main__":
    Test().run()
