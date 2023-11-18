import pygame


class Input:
    def __init__(self):
        self.quit = False

        self.key_down_list = []
        self.key_pressed_list = []
        self.key_up_list = []

    def update(self):
        self.key_down_list = []
        self.key_up_list = []

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.quit = True
                case pygame.KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    self.key_down_list.append(key_name)
                    self.key_pressed_list.append(key_name)
                case pygame.KEYUP:
                    key_name = pygame.key.name(event.key)
                    self.key_pressed_list.remove(key_name)
                    self.key_up_list.append(key_name)

    def is_key_down(self, key_code: str) -> bool:
        return key_code in self.key_down_list

    def is_key_up(self, key_code: str) -> bool:
        return key_code in self.key_up_list

    def is_key_pressed(self, key_code: str) -> bool:
        return key_code in self.key_pressed_list
