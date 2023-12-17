from core.data_type import DataType
from core.texture import Texture
from material.material import Material
from OpenGL import GL


class SpriteMaterial(Material):
    def __init__(self, texture: Texture, properties=None):
        if properties is None:
            properties = {}
        vertex_shader_code = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        uniform bool billboard;
        uniform float tileNumber;
        uniform vec2 tileCount;
        in vec3 vertexPosition;
        in vec2 vertexUV;
        out vec2 UV;

        void main()
        {
            mat4 mvMatrix = viewMatrix * modelMatrix;
            if ( billboard )
            {
                mvMatrix[0][0] = 1;
                mvMatrix[0][1] = 0;
                mvMatrix[0][2] = 0;
                mvMatrix[1][0] = 0;
                mvMatrix[1][1] = 1;
                mvMatrix[1][2] = 0;
                mvMatrix[2][0] = 0;
                mvMatrix[2][1] = 0;
                mvMatrix[2][2] = 1;
            }
            gl_Position = projectionMatrix * mvMatrix * vec4( vertexPosition, 1.0);
            UV = vertexUV;
            if ( tileNumber > -1.0)
            {
                vec2 tileSize = 1.0 / tileCount;
                float ColumnIndex = mod(tileNumber, tileCount[0]);
                float rowIndex = floor(tileNumber / tileCount[0]);
                vec2 tileOffset = vec2(ColumnIndex/ tileCount[0], 1.0 - (rowIndex + 1.0)/tileCount[1]);
                UV = UV * tileSize + tileOffset;
            }

        }
        """
        fragment_shader_code = """
        uniform vec3 baseColor;
        uniform sampler2D texture;
        in vec2 UV;
        out vec4 fragColor;

        void main()
        {
            vec4 color = vec4(baseColor, 1) * texture2D(texture, UV);
            if (color.a < 0.1)
            {
                discard;
            }
            fragColor = color;
        }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform(DataType.vec3, "baseColor", [1.0, 1.0, 1.0])
        self.add_uniform(
            DataType.sampler2D, "texture", [
                texture.texture_ref, 1])
        self.add_uniform(DataType.bool, "billboard", False)
        self.add_uniform(DataType.float, "tileNumber", -1)
        self.add_uniform(DataType.vec2, "tileCount", [1.1])
        self.locate_uniforms()

        self.settings["doubleSide"] = True
        self.set_properties(properties)

    def update_render_settings(self):
        if self.settings["doubleSide"]:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)
