from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight
from material.phong_material import PhongMaterial
from geometry.rectangle_geometry import  RectangleGeometry
from geometry.sphere_geometry import SphereGeometry
from extras.movement_rig import MovementRig
from extras.directional_light_helper import DirectionalLightHelper

class Test(Base)
    def initialize(self):
        pass