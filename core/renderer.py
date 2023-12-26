from OpenGL import GL

from core.camera import Camera
from core.mesh import Mesh
from core.render_target import RenderTarget
from core.scene import Scene
from light.light import Light
from light.shadow import Shadow
import pygame


class Renderer:
    def __init__(self, clear_color=(0, 0, 0)):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)
        GL.glEnable(GL.GL_BLEND)

        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glClearColor(*clear_color, 1)

        self.window_size = pygame.display.get_surface().get_size()
        self.shadow_enabled = False

    def enable_shadows(self, shadow_light: Light,
                       strength=0.5, resolution=(512, 512)):
        self.shadow_enabled = True
        self.shadow_object = Shadow(
            shadow_light,
            strength=strength,
            resolution=resolution)

    def render(self, scene: Scene, camera: Camera,
               clear_color=True, clear_depth=True, render_target: RenderTarget = None):
        if clear_color:
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        if clear_depth:
            GL.glClear(GL.GL_DEPTH_BUFFER_BIT)

        camera.update_view_matrix()

        if render_target is None:
            GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
            GL.glViewport(0, 0, *self.window_size)
        else:
            GL.glBindFramebuffer(
                GL.GL_FRAMEBUFFER,
                render_target.frame_buffer_ref)
            GL.glViewport(0, 0, render_target.width, render_target.height)

        descendant_list = scene.get_descendant_list()
        def mesh_filter(x): return isinstance(x, Mesh)
        mesh_list = list(filter(mesh_filter, descendant_list))
        if self.shadow_enabled:
            GL.glBindFramebuffer(
                GL.GL_FRAMEBUFFER,
                self.shadow_object.render_target.frame_buffer_ref)
            GL.glViewport(
                0,
                0,
                self.shadow_object.render_target.width,
                self.shadow_object.render_target.height)
            GL.glClearColor(1, 1, 1, 1)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
            GL.glClear(GL.GL_DEPTH_BUFFER_BIT)
            GL.glUseProgram(self.shadow_object.material.program_ref)

            self.shadow_object.update_internal()

            for mesh in mesh_list:
                if not mesh.visible:
                    continue
                if mesh.material.settings["drawStyle"] != GL.GL_TRIANGLES:
                    continue
                GL.glBindVertexArray(mesh.vao_ref)
                self.shadow_object.material.uniforms["modelMatrix"].data = mesh.get_world_matrix(
                )
                for var_name, unif_obj in self.shadow_object.material.uniforms.items():
                    unif_obj.upload_data()
                GL.glDrawArrays(GL.GL_TRIANGLES, 0, mesh.geometry.vertex_count)

        def light_filter(x): return isinstance(x, Light)
        light_list = list(filter(light_filter, descendant_list))

        while len(light_list) < 4:
            light_list.append(Light())

        for mesh in mesh_list:
            if not mesh.visible:
                continue
            GL.glUseProgram(mesh.material.program_ref)
            GL.glBindVertexArray(mesh.vao_ref)
            mesh.material.uniforms["modelMatrix"].data = mesh.get_world_matrix(
            )
            mesh.material.uniforms["viewMatrix"].data = camera.view_matrix
            mesh.material.uniforms["projectionMatrix"].data = camera.projection_matrix

            if self.shadow_enabled and "shadow0" in mesh.material.uniforms.keys():
                mesh.material.uniforms["shadow0"].data = self.shadow_object

            if "light0" in mesh.material.uniforms.keys():
                for light_number in range(4):
                    light_name = f"light{light_number}"
                    light_object = light_list[light_number]
                    mesh.material.uniforms[light_name].data = light_object
            if "viewPosition" in mesh.material.uniforms.keys():
                mesh.material.uniforms["viewPosition"].data = camera.get_world_position(
                )

            for variable_name, uniform_object in mesh.material.uniforms.items():
                uniform_object.upload_data()

            mesh.material.update_render_settings()
            GL.glDrawArrays(
                mesh.material.settings["drawStyle"],
                0,
                mesh.geometry.vertex_count)
