from geometry.sphere_geometry import SphereGeometry
from material.surface_material import SurfaceMaterial
from core.mesh import Mesh
from light.point_light import PointLight


class PointLightHelper(Mesh):

    def __init__(self, point_light: PointLight, size=0.1, line_width=1):
        color = point_light.color
        geometry = SphereGeometry(radius=size, radius_segments=4, height_segments=2)
        material = SurfaceMaterial(
            {
                "baseColor": color,
                "wireframe": True,
                "doubleSide": True,
                "lineWidth": line_width,
            }
        )
        super().__init__(geometry, material)
