from core.base import Base
from core.data_type import DataType
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.rectangle_geometry import RectangleGeometry
from material.material import Material
from core.texture import Texture


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
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            UV = vertexUV;
        }
        """
        fragment_shader_code = """
        uniform sampler2D noise;
        uniform sampler2D image;
        in vec2 UV;
        uniform float time;
        out vec4 fragColor;

        void main()
        {
            vec2 uvShift = UV + vec2( -0.033, 0.07 ) * time;
            vec4 noiseValues = texture2D ( noise, uvShift );
            vec2 uvNoise = UV + 0.4 * noiseValues.rg;
            fragColor = texture2D(image, uvNoise);
        }
        """
        noise_text = Texture("../images/rgb-noise.jpg")
        gird_text = Texture("../images/grid.jpg")

        self.distort_material = Material(vertex_shader_code, fragment_shader_code)
        self.distort_material.add_uniform(
            DataType.sampler2D, "noise", [noise_text.texture_ref, 1]
        )
        self.distort_material.add_uniform(
            DataType.sampler2D, "image", [gird_text.texture_ref, 2]
        )
        self.distort_material.add_uniform(DataType.float, "time", 0.0)
        self.distort_material.locate_uniforms()

        geometry = RectangleGeometry()
        self.mesh = Mesh(geometry, self.distort_material)
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.distort_material.uniforms["time"].data += self.delta_time


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
