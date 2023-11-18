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

        self.translation = Uniform(DataType.vec3, [-0.5, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, "translation")

        self.base_color = Uniform(DataType.vec3, [1.0, 0.0, 0.0])
        self.base_color.locate_variable(self.program_ref, "baseColor")

        self.speed = 1.5

    def update(self):

        distance = self.speed * self.delta_time

        if self.translation.data[0] > 1.2:
            self.translation.data[0] = -1.2

        if self.translation.data[0] < -1.2:
            self.translation.data[0] = 1.2

        if self.translation.data[1] > 1.2:
            self.translation.data[1] = -1.2

        if self.translation.data[1] < -1.2:
            self.translation.data[1] = 1.2

        if self.input.is_key_pressed("left"):
            self.translation.data[0] -= distance
        if self.input.is_key_pressed("right"):
            self.translation.data[0] += distance
        if self.input.is_key_pressed("down"):
            self.translation.data[1] -= distance
        if self.input.is_key_pressed("up"):
            self.translation.data[1] += distance

        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(self.program_ref)

        self.translation.upload_data()
        self.base_color.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)


if __name__ == "__main__":
    Test().run()
