import pygame
from abc import ABC, abstractmethod
import sys

from core.input import Input


class Base(ABC):
    def __init__(self, screen_size: tuple[int, int] = (512, 512)):
        pygame.init()
        display_flags = pygame.DOUBLEBUF | pygame.OPENGL
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
        )

        self.screen = pygame.display.set_mode(screen_size, display_flags)

        pygame.display.set_caption("Graphic Window")
        self.running = True
        self.clock = pygame.time.Clock()

        self.input = Input()

        self.time = 0

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def update(self):
        pass

    def run(self):
        self.initialize()
        while self.running:

            self.input.update()
            if self.input.quit:
                self.running = False

            self.delta_time = self.clock.get_time() / 1000
            self.time += self.delta_time

            self.update()

            # render
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
