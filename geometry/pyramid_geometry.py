from geometry.cylindrical_geometry import CylindricalGeometry


class PyramidGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1, sides=4, height_segments=4, closed=True):
        super().__init__(0, radius, height, sides, height_segments, False, closed)
