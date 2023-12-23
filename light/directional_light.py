from light.light import Light, LightType


class DirectionalLight(Light):
    def __init__(self, color=(1, 1, 1), direction=(0, -1, 0)):
        super().__init__(LightType.DIRECTIONAL)
        self.color = color
        self.set_direction(direction)
