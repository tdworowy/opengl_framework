from geometry.cylindrical_geometry import CylindricalGeometry


class ConeGeometry(CylindricalGeometry):
    def __init__(
        self, radius=1, height=1, radial_segments=32, height_segments=4, closed=True
    ):
        super().__init__(
            0, radius, height, radial_segments, height_segments, False, closed
        )
