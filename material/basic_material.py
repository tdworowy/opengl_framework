from core.data_type import DataType
from material.material import Material


class BasicMaterial(Material):
    def __init__(self):
        vertex_shader_code = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec3 vertexColor;
        out vect3 color;

        void main()
        {
            gl_position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            color = vertexColor;
        }
        """
        fragment_shader_code = """
        uniform vec3 baseColor;
        uniform bool userVertexColors;
        in vec3 color;
        out vec4 fragColor;

        void main()
        {
            vec4 tempColor = vec4(baceColor, 1.0);
            if (useVertexColors)
                tempColor *=vec4(color, 1.0);
            fragColor = tempColor;
        }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform(DataType.vec3, "baseColor", [1.0, 1.0, 1.0])
        self.add_uniform(DataType.bool, "userVertexColors", False)

        self.locate_uniforms()
