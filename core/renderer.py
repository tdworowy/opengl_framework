from OpenGL import GL

from core.camera import Camera
from core.mesh import Mesh
from core.scene import Scene


class Renderer:
    def __init__(self, clear_Color=None):
        if clear_Color is None:
            clear_Color = [0, 0, 0]

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)
        GL.glEnable(GL.GL_BLEND)

        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glClearColor(clear_Color[0], clear_Color[1], clear_Color[2], 1)

    def render(self, scene: Scene, camera: Camera):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        camera.update_view_matrix()
        descendant_list = scene.get_descendant_list()
        def mesh_filter(x): return isinstance(x, Mesh)
        mesh_list = list(filter(mesh_filter, descendant_list))

        for mesh in mesh_list:
            if not mesh.visible:
                continue
            GL.glUseProgram(mesh.material.program_ref)
            GL.glBindVertexArray(mesh.vao_ref)
            mesh.material.uniforms["modelMatrix"].data = mesh.get_world_matrix(
            )
            mesh.material.uniforms["viewMatrix"].data = camera.view_matrix
            mesh.material.uniforms["projectionMatrix"].data = camera.projection_matrix

            for variable_name, uniform_object in mesh.material.uniforms.items():
                uniform_object.upload_data()

            mesh.material.update_render_settings()
            GL.glDrawArrays(
                mesh.material.settings["drawStyle"],
                0,
                mesh.geometry.vertex_count)
