from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.sphere_geometry import SphereGeometry
from material.material import Material


class Test(Base):

    def initialize(self):
        print("Initializing program....")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.camera.set_position([0, 0, 7])

        geometry = SphereGeometry(radius=9)  # 4 or less for normal sphere
        vs_code = """
        in vec3 vertexPosition;
        out vec3 position;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        void main()
        {
            vec4 pos = vec4(vertexPosition, 1.0);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
            position = vertexPosition;
        }
        """
        fs_code = """
        in vec3 position;
        out vec4 fragColor;
        void main()
        {
            vec3 color = mod(position, 1.0);
            fragColor = vec4(color, 1.0);
        }
        """
        material = Material(vs_code, fs_code)
        material.locate_uniforms()

        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)
        # self.mesh.rotate_x(0.00514)
        # self.mesh.rotate_y(0.0514)
        # self.mesh.rotate_z(0.00514)
        self.mesh.rotate_x(0.514)
        self.mesh.rotate_y(0.514)
        self.mesh.rotate_z(0.514)


if __name__ == "__main__":
    Test(screen_size=(800, 600)).run()
