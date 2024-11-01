from core.data_type import DataType
from effects.base_effect import BaseEffect


class VignetteEffect(BaseEffect):

    def __init__(self, dimming_start=0.4, dimming_end=1.0, dimming_color=(0, 0, 0)):
        vertex_shader_code = """
           in vec2 vertexPosition;
           in vec2 vertexUV;
           out vec2 UV;

           void main()
           {
               gl_Position = vec4(vertexPosition, 0.0, 1.0);
               UV = vertexUV;
           }
           """
        fragment_shader_code = """
           in vec2 UV;
           uniform sampler2D textureSampler;
           uniform float dimStart;
           uniform float dimEnd;
           uniform vec3 dimColor;
           out vec4 fragColor;

           void main()
           {
               vec4 color = Sample(textureSampler, UV);
               vec2 position = 2 * UV - vec2(1, 1);
               float d = length(position);
               float b = (d - dimEnd) / (dimStart - dimEnd);
               b = clamp(b, 0, 1);
               fragColor = vec4(b * color.rgb + (1 - b) * dimColor, 1);
           }
           """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform(DataType.sampler2D, "texture", [None, 1])
        self.add_uniform(DataType.float, "dimStart", dimming_start)
        self.add_uniform(DataType.float, "dimEnd", dimming_end)
        self.add_uniform(DataType.vec3, "dimColor", dimming_color)
        self.locate_uniforms()
