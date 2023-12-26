from core.camera import Camera
from core.render_target import RenderTarget
from light.light import Light
from material.depth_material import DepthMaterial
from OpenGL import GL


class Shadow:
    def __init__(self, light_source: Light, strength=0.5, resolution=(
            512, 512), camera_bounds=(-5, 5, -5, 5, 0, 20), bias=0.01):
        self.light_source = light_source
        self.camera = Camera()
        self.camera.set_orthographic(*camera_bounds)
        self.light_source.add(self.camera)

        self.render_target = RenderTarget(
            resolution, properties={
                "wrap": GL.GL_CLAMP_TO_BORDER})
        self.material = DepthMaterial()

        self.strength = strength
        self.bias = bias

    def update_internal(self):
        self.camera.update_view_matrix()
        self.material.uniforms["viewMatrix"].data = self.camera.view_matrix
        self.material.uniforms["projectionMatrix"].data = self.camera.projection_matrix
