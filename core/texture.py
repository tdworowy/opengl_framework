import pygame
from OpenGL import GL


class Texture:
    def __init__(self, file_name=None, properties=None):
        if properties is None:
            properties = {}

        self.surface = None
        self.texture_ref = GL.glGenTextures(1)

        self.properties = {
            "magFilter": GL.GL_LINEAR,
            "minFilter": GL.GL_LINEAR_MIPMAP_LINEAR,
            "wrap": GL.GL_REPEAT
        }

        self.set_properties(properties)

        if file_name is not None:
            self.load_image(file_name)
            self.upload_data()

    def load_image(self, file_name: str):
        self.surface = pygame.image.load(file_name)

    def set_properties(self, props: dict):
        for name, data in props.items():
            if name in self.properties.keys():
                self.properties[name] = data
            else:
                raise Exception(f"Texture has no property: {name}")

    def upload_data(self):
        width = self.surface.get_width()
        height = self.surface.get_height()

        pixel_data = pygame.image.tostring(self.surface, "RGBA", True)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_ref)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGBA,
            width,
            height,
            0,
            GL.GL_RGBA,
            GL.GL_UNSIGNED_BYTE,
            pixel_data)
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

        GL.glTexParameteri(
            GL.GL_TEXTURE_2D,
            GL.GL_TEXTURE_MAG_FILTER,
            self.properties["magFilter"])
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D,
            GL.GL_TEXTURE_MIN_FILTER,
            self.properties["minFilter"])

        GL.glTexParameteri(
            GL.GL_TEXTURE_2D,
            GL.GL_TEXTURE_WRAP_S,
            self.properties["wrap"])
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D,
            GL.GL_TEXTURE_WRAP_T,
            self.properties["wrap"])

        GL.glTexParameterfv(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_BORDER_COLOR, [
                1, 1, 1, 1])
