from OpenGL import GL
import pygame
from core.texture import Texture

# TODO something is wrong with it


class RenderTarget:
    def __init__(self, resolution=(512, 512), texture: Texture = None, properties=None):
        if properties is None:
            properties = {}

        self.width, self.height = resolution
        if texture is not None:
            self.texture = texture
        else:
            self.texture = Texture(
                properties={
                    "magFilter": GL.GL_LINEAR,
                    "minFilter": GL.GL_LINEAR,
                    "wrap": GL.GL_CLAMP_TO_EDGE,
                }
            )
            self.texture.set_properties(properties)
            self.texture.surface = pygame.Surface(resolution)
            self.texture.upload_data()

        self.frame_buffer_ref = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.frame_buffer_ref)
        GL.glFramebufferTexture(
            GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, self.frame_buffer_ref, 0
        )

        depth_buffer_ref = GL.glGenRenderbuffers(1)
        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, depth_buffer_ref)
        GL.glRenderbufferStorage(
            GL.GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT, self.width, self.height
        )
        GL.glFramebufferRenderbuffer(
            GL.GL_FRAMEBUFFER,
            GL.GL_DEPTH_ATTACHMENT,
            GL.GL_RENDERBUFFER,
            depth_buffer_ref,
        )

        if GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER) != GL.GL_FRAMEBUFFER_COMPLETE:
            raise Exception("Framebuffer status error")
