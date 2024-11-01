from core.data_type import DataType
from core.texture import Texture
from material.material import Material
from OpenGL import GL


class FlatMaterial(Material):
    def __init__(self, texture: Texture = None, properties=None):
        if properties is None:
            properties = {}

        vertex_shader_code = """
        struct Light
        {
            int lightType;
            vec3 color;
            vec3 direction;
            vec3 position;
            vec3 attenuation;
        };
        uniform Light light0;
        uniform Light light1;
        uniform Light light2;
        uniform Light light3;

        vec3 lightCalc(Light light, vec3 pointPosition, vec3 pointNormal)
        {
            float ambient = 0;
            float diffuse = 0;
            float specular = 0;
            float attenuation = 1;
            vec3 lightDirection = vec3(0,0,0);
            if ( light.lightType == 1)
            {
                ambient = 1;
            }
            else if ( light.lightType == 2)
            {
                lightDirection = normalize(light.direction);
            }
            else if ( light.lightType == 3)
            {
               lightDirection = normalize(pointPosition - light.position);
               float distance = length(light.position - pointPosition);
               attenuation = 1.0 / (light.attenuation[0] + light.attenuation[1] * distance + light.attenuation[2] * distance * distance);
            }
            if (light.lightType > 1)
            {
                pointNormal = normalize(pointNormal);
                diffuse = max(dot(pointNormal, -lightDirection),0.0);
                diffuse *= attenuation;
            }
            return light.color * (ambient + diffuse + specular);
        }

        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec2 vertexUV;
        in vec3 faceNormal;
        out vec2 UV;
        out vec3 light;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
            UV = vertexUV;
            vec3 position = vec3(modelMatrix * vec4(vertexPosition, 1));
            vec3 normal = normalize(mat3(modelMatrix) * faceNormal);
            light = vec3(0, 0, 0);
            light += lightCalc( light0, position, normal);
            light += lightCalc( light1, position, normal);
            light += lightCalc( light2, position, normal);
            light += lightCalc( light3, position, normal);
        }

        """
        fragment_shader_code = """
        uniform vec3 baseColor;
        uniform bool useTexture;
        uniform sampler2D textureSampler;
        in vec2 UV;
        in vec3 light;
        out vec4 fragColor;

        void main()
        {
            vec4 color = vec4(baseColor, 1.0);
            if (useTexture)
            {
                color *= texture(textureSampler, UV);
            }
            color *=vec4(light, 1);
            fragColor = color;
        }
        """

        super().__init__(vertex_shader_code, fragment_shader_code)

        self.add_uniform(DataType.vec3, "baseColor", [1.0, 1.0, 1.0])
        self.add_uniform(DataType.light, "light0", None)
        self.add_uniform(DataType.light, "light1", None)
        self.add_uniform(DataType.light, "light2", None)
        self.add_uniform(DataType.light, "light3", None)
        self.add_uniform(DataType.bool, "useTexture", 0)

        if texture is None:
            self.add_uniform(DataType.bool, "useTexture", False)
        else:
            self.add_uniform(DataType.bool, "useTexture", True)
            self.add_uniform(
                DataType.sampler2D, "textureSampler", [texture.texture_ref, 1]
            )

        self.locate_uniforms()

        self.settings["doubleSide"] = True
        self.settings["wireFrame"] = False
        self.settings["lineWidth"] = 1

        self.set_properties(properties)

    def update_render_settings(self):
        if self.settings["doubleSide"]:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)

        if self.settings["wireFrame"]:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glLineWidth(self.settings["lineWidth"])
