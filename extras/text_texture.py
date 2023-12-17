from core.texture import Texture
import pygame


class TextTexture(Texture):

    def __init__(self, text="Hello World!", system_font_name="Helvetica Standard", font_file_name=None, font_size=24,
                 font_color=None, background_color=None, transparent=False, image_width=None, image_height=None,
                 align_horizontal=0.0, align_vertical=0.0, image_border_width=0, image_border_color=None):
        if image_border_color is None:
            image_border_color = [0, 0, 0]
        if background_color is None:
            background_color = [255, 255, 255]
        if font_color is None:
            font_color = [0, 0, 0]

        super().__init__()

        font = pygame.font.SysFont(system_font_name, font_size)
        if font_file_name is not None:
            font = pygame.font.Font(font_file_name, font_size)
        font_surface = font.render(text, True, font_color)
        (text_width, text_height) = font.size(text)

        if image_width is None:
            image_width = text_width
        if image_height is None:
            image_height = text_height

        self.surface = pygame.Surface(
            (image_width, image_height), pygame.SRCALPHA)
        if not transparent:
            self.surface.fill(background_color)

        corner_point = (align_horizontal * (image_width - text_width),
                        align_vertical * (image_height - text_height))

        destination_rectangle = font_surface.get_rect(topleft=corner_point)
        if image_border_width > 0:
            pygame.draw.rect(
                self.surface, image_border_color, [
                    0, 0, image_width, image_height], image_border_width)

        self.surface.blit(font_surface, destination_rectangle)
        self.upload_data()
