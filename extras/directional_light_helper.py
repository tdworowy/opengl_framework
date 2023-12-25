from extras.grid_helper import GridHelper
from light.directional_light import DirectionalLight


class DirectionalLightHelper(GridHelper):

    def __init__(self, directional_light: DirectionalLight):
        color = directional_light.color
        super().__init__(size=1, divisions=4, grid_color=color, center_color=(1, 1, 1))

        self.geometry.attributes["vertexPosition"].data += [[0,
                                                             0, 0], [0, 0, -10]]
        self.geometry.attributes["vertexColor"].data += [color, color]

        self.geometry.attributes["vertexPosition"].upload_data()
        self.geometry.attributes["vertexColor"].upload_data()

        self.geometry.count_vertices()
