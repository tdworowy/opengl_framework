from core.object3D import Object3D


from enum import IntEnum


class LightType(IntEnum):
    ZERO = 0
    AMBIENT = 1
    DIRECTIONAL = 2
    POINT = 3


class Light(Object3D):
    def __init__(self, light_type: LightType = LightType.ZERO):
        super().__init__()
        self.light_type = light_type
        self.color = (1, 1, 1)
        self.attenuation = (1, 0, 0)
