from geometry.parametric_geometry import ParametricGeometry


class PlaneGeometry(ParametricGeometry):
    def __init__(self, width=1, height=1, width_segment=8, height_segment=8):
        def s(u, v):
            return [u, v, 0]

        super().__init__(
            -width / 2,
            width / 2,
            width_segment,
            -height / 2,
            height / 2,
            height_segment,
            s,
        )
