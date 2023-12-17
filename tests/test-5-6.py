from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.rectangle_geometry import RectangleGeometry
from material.material import Material
from core.texture import Texture
from material.texture_material import TextureMaterial


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.camera.set_position([0, 0, 1.5])

        vertex_shader_code = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec2 vertexUV;
        out vec2 UV;

        void main()
        {
            vec4 pos = vec4(vertexPosition, 1.0);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
            UV = vertexUV;
        }
        """
        fragment_shader_code = """
        float random(vec2 UV)
        {
            return fract(235711.0 * sin(14.337 * UV.x + 42.418 * UV.y));
        }
        float boxRandom(vec2 UV, float scale)
        {
            vec2 iScaleUV = floor(scale * UV);
            return random(iScaleUV);
        }
        float smoothRandom(vec2 UV, float scale)
        {
            vec2 iScaleUV = floor(scale * UV);
            vec2 fScaleUV = floor(scale * UV);
            float a = random(iScaleUV);
            float b = random(round(iScaleUV + vec2(1, 0)));
            float c = random(round(iScaleUV + vec2(0, 1)));
            float d = random(round(iScaleUV + vec2(1, 1)));
            return mix(mix(a, b, fScaleUV.x),
                       mix(c, d, fScaleUV.x),
                       fScaleUV.y);

        }
        float fractalRandom(vec2 UV, float scale)
        {
            float value = 0.0;
            float amplitude = 0.5;
            for(int i = 0; i < 6; i++)
            {
                value += amplitude * smoothRandom(UV, scale);
                scale *=2.0;
                amplitude *=0.5;
            }
            return value;
        }

        in vec2 UV;
        out vec4 fragColor;

        void main()
        {
            float r =  fractalRandom(UV, 5);
            vec4 color1 = vec4(0.5, 0.5, 1, 1);
            vec4 color2 = vec4(1, 1, 1, 1);
            fragColor = mix(color1, color2, r);
        }
        """
        geometry = RectangleGeometry()
        material = Material(vertex_shader_code, fragment_shader_code)
        material.locate_uniforms()
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
