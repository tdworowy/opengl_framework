from core.data_type import DataType
from core.texture import Texture
from material.material import Material
from OpenGL import GL


class TextureMaterial(Material):

    def __init__(self, texture: Texture, properties=None):
        if properties is None:
            properties = {}
        vertex_shader_code = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec2 vertexUV;
        uniform vec2 repeatUV;
        uniform vec2 offsetUV;
        out vec2 UV;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            UV = vertexUV * repeatUV  + offsetUV;
        }
        """

        fragment_shader_code = """
        uniform vec3 baseColor;
        uniform sampler2D texture;
        in vec2 UV;
        out vec4 fragColor;

        void main()
        {
            vec4 color = vec4(baseColor, 1.0) * texture2D(texture, UV);
            if(color.a < 0.10)
                discard;
            fragColor = color;
        }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)

        self.add_uniform(DataType.vec3, "baseColor", [1.0, 1.0, 1.0])
        self.add_uniform(
            DataType.sampler2D, "texture", [
                texture.texture_ref, 1])
        self.add_uniform(DataType.vec2, "repeatUV", [1.0, 1.0])
        self.add_uniform(DataType.vec2, "offsetUV", [0.0, 0.0])

        self.locate_uniforms()

        self.settings["doubleSide"] = True
        self.settings["wireframe"] = False
        self.settings["lineWidth"] = 1

        self.set_properties(properties)

    def update_render_settings(self):
        if self.settings["doubleSide"]:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)
        if self.settings["wireframe"]:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

        GL.glLineWidth(self.settings["lineWidth"])
