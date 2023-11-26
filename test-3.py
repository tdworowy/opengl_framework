from core.base import Base
from core.data_type import DataType
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from core.matrix import Matrix
from OpenGL.GL import *
from math import pi


class Test(Base):

    def initialize(self):
        print("Initializing program...")

        vs_code = """
        in vec3 position;
        uniform mat4 projectionMatrix;
        uniform mat4 modelMatrix;
        void main()
        {
            gl_Position = projectionMatrix * modelMatrix * vec4(position, 1.0);
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

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        position_data = [[0.0, 0.2, 0.0],
                         [0.1, -0.2, 0.0],
                         [-0.1, -0.2, 0.0]]
        self.vertex_count = len(position_data)
        position_attribute = Attribute(DataType.vec3, position_data)
        position_attribute.associate_variable(self.program_ref, "position")

        m_matrix = Matrix.make_translation(0, 0, -1)
        self.model_matrix = Uniform(DataType.mat4, m_matrix)
        self.model_matrix.locate_variable(self.program_ref, "modelMatrix")

        p_matrix = Matrix.make_perspective()
        self.projection_matrix = Uniform(DataType.mat4, p_matrix)
        self.projection_matrix.locate_variable(
            self.program_ref, "projectionMatrix")

        self.move_speed = 0.5
        self.turn_speed = 90 * (pi / 180)

    def update(self):
        move_amount = self.move_speed * self.delta_time
        turn_amount = self.turn_speed * self.delta_time

        if self.input.is_key_pressed("w"):
            m = Matrix.make_translation(0, move_amount, 0)
            self.model_matrix.data = m @ self.model_matrix.data

        if self.input.is_key_pressed("s"):
            m = Matrix.make_translation(0, -move_amount, 0)
            self.model_matrix.data = m @ self.model_matrix.data

        if self.input.is_key_pressed("a"):
            m = Matrix.make_translation(-move_amount, 0, 0)
            self.model_matrix.data = m @ self.model_matrix.data

        if self.input.is_key_pressed("d"):
            m = Matrix.make_translation(move_amount, 0, 0)
            self.model_matrix.data = m @ self.model_matrix.data

        if self.input.is_key_pressed("z"):
            m = Matrix.make_translation(0, 0, move_amount)
            self.model_matrix.data = m @ self.model_matrix.data

        if self.input.is_key_pressed("x"):
            m = Matrix.make_translation(0, 0, -move_amount)
            self.model_matrix.data = m @ self.model_matrix.data

        if self.input.is_key_pressed("q"):
            m = Matrix.make_rotation_z(turn_amount)
            self.model_matrix.data = m @ self.model_matrix.data

        if self.input.is_key_pressed("e"):
            m = Matrix.make_rotation_z(-turn_amount)
            self.model_matrix.data = m @ self.model_matrix.data

        if self.input.is_key_pressed("i"):
            m = Matrix.make_translation(0, move_amount, 0)
            self.model_matrix.data = self.model_matrix.data @ m

        if self.input.is_key_pressed("k"):
            m = Matrix.make_translation(0, -move_amount, 0)
            self.model_matrix.data = self.model_matrix.data  @ m

        if self.input.is_key_pressed("j"):
            m = Matrix.make_translation(-move_amount, 0, 0)
            self.model_matrix.data = self.model_matrix.data  @ m

        if self.input.is_key_pressed("l"):
            m = Matrix.make_translation(move_amount, 0, 0)
            self.model_matrix.data = self.model_matrix.data  @ m

        if self.input.is_key_pressed("u"):
            m = Matrix.make_rotation_z(turn_amount)
            self.model_matrix.data = self.model_matrix.data @ m

        if self.input.is_key_pressed("o"):
            m = Matrix.make_rotation_z(-turn_amount)
            self.model_matrix.data = self.model_matrix.data @ m

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_ref)
        self.projection_matrix.upload_data()
        self.model_matrix.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)


if __name__ == "__main__":
    Test().run()
