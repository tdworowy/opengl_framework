from light.light import Light, LightType


class AmbientLight(Light):

    def __init__(self, color=(1, 1, 1)):
        super().__init__(LightType.AMBIENT)
        self.color = color
