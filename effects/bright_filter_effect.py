from core.data_type import DataType
from effects.base_effect import BaseEffect


class BrightFilterEffect(BaseEffect):

    def __init__(self, threshold=2.4):
        vertex_shader_code = """
        in vec2 vertexPosition;
        in vec2 vertexUV;
        out vec2 UV;
        void main()
        {
            gl_Position = vec4(vertexPosition, 0.0, 1.0);
            UV =vertexUV;
        }
        """
        fragment_shader_code = """
        in vec2 UV;
        uniform sampler2D textureSampler;
        uniform float threshold;
        out vec4 fragColor;
        void main()
        {
            vec4 color = texture(textureSampler, UV);
            if(color.r + color.g + color.b < threshold)
            {
                discard;
            }
            fragColor = color;
        }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform(DataType.sampler2D, "textureSampler", [None, 1])
        self.add_uniform(DataType.float, "threshold", threshold)
        self.locate_uniforms()
