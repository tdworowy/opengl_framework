from core.data_type import DataType
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.render_target import RenderTarget
from effects.base_effect import BaseEffect
from geometry.geometry import Geometry


class Postprocessor:

    def __init__(self, renderer: Renderer, scene: Scene,
                 camera: Camera, final_render_target=None):
        self.renderer = renderer
        self.scene_list = [scene]
        self.camera_list = [camera]
        self.render_target_list = [final_render_target]
        self.final_render_target = final_render_target

        self.ortho_camera = Camera()
        self.ortho_camera.set_orthographic()

        self.rectangle_geometry = Geometry()
        P0, P1, P2, P3 = [-1, -1], [1, -1], [-1, 1], [1, 1]
        T0, T1, T2, T3 = [0, 0], [1, 0], [0, 1], [1, 1]

        position_data = [P0, P1, P3, P0, P3, P2]
        uv_data = [T0, T1, T3, T0, T3, T2]

        self.rectangle_geometry.add_attribute(
            DataType.vec2, "vertexPosition", position_data)
        self.rectangle_geometry.add_attribute(
            DataType.vec2, "vertexUV", uv_data)
        self.rectangle_geometry.count_vertices()

    def add_effect(self, effect: BaseEffect):
        post_scene = Scene()
        resolution = self.renderer.window_size
        target = RenderTarget(resolution)
        self.render_target_list[-1] = target
        effect.uniforms["textureSampler"].data[0] = target.texture.texture_ref

        mesh = Mesh(self.rectangle_geometry, effect)
        post_scene.add(mesh)

        self.scene_list.append(post_scene)
        self.camera_list.append(self.ortho_camera)
        self.render_target_list.append(self.final_render_target)

    def render(self):
        passes = len(self.scene_list)
        for n in range(passes):
            scene = self.scene_list[n]
            camera = self.camera_list[n]
            target = self.render_target_list[n]
            self.renderer.render(scene, camera, render_target=target)
