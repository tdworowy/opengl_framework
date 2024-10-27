from core.data_type import DataType
from core.texture import Texture
from material.material import Material
from OpenGL import GL


class PhongMaterial(Material):
    def __init__(
        self,
        texture: Texture = None,
        properties=None,
        bump_texture=None,
        use_shadow=False,
    ):
        if properties is None:
            properties = {}

        vertex_shader_code = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec2 vertexUV;
        in vec3 vertexNormal;
        out vec3 position;
        out vec2 UV;
        out vec3 normal;

        struct Shadow
        {
            vec3 lightDirection;
            mat4 projectionMatrix;
            mat4 viewMatrix;
            sampler2D depthTextureSampler;
            float strength;
            float bias;

        };
        uniform bool useShadow;
        uniform Shadow shadow0;
        out vec3 shadowPosition0;

        void main()
        {
           if( useShadow )
           {
              vec4 temp0 = shadow0.projectionMatrix * shadow0.viewMatrix * modelMatrix * vec4(vertexPosition, 1);
              shadowPosition0 = vec3(temp0);
           }
           gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
           position = vec3 (modelMatrix * vec4(vertexPosition,1));
           UV = vertexUV;
           normal = normalize(mat3(modelMatrix) * vertexNormal);
        }
        """
        fragment_shader_code = """
        struct Light
        {
            int lightType;
            vec3 color;
            vec3 direction;
            vec3 position;
            vec3 attenuation;
        };
        uniform vec3 viewPosition;
        uniform float specularStrength;
        uniform float shininess;
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
                if(diffuse >0)
                {
                    vec3 viewDirection = normalize(viewPosition - pointPosition);
                    vec3 reflectDirection = reflect(lightDirection, pointNormal);
                    specular = max(dot(viewDirection, reflectDirection), 0.0);
                    specular = specularStrength * pow(specular,shininess);
                }
            }
            return light.color * (ambient + diffuse + specular);
        }
        uniform vec3 baseColor;
        uniform bool useTexture;
        uniform sampler2D textureSampler;
        uniform bool useBumpTexture;
        uniform sampler2D bumpTextureSampler;
        uniform float bumpStrength;
        in vec3 position;
        in vec2 UV;
        in vec3 light;
        in vec3 normal;
        out vec4 fragColor;

        struct Shadow
        {
            vec3 lightDirection;
            mat4 projectionMatrix;
            mat4 viewMatrix;
            sampler2D depthTextureSampler;
            float strength;
            float bias;

        };
        uniform bool useShadow;
        uniform Shadow shadow0;
        out vec3 shadowPosition0;

        void main()
        {
            vec4 color = vec4(baseColor, 1.0);
            if (useTexture)
            {
                color *= texture(textureSampler, UV);
            }
            vec3 bNormal = normal;
            if (useBumpTexture)
            {
                bNormal += bumpStrength * vec3(texture(bumpTextureSampler, UV));
            }
            vec3 total = vec3(0, 0, 0);
            total += lightCalc( light0, position, bNormal);
            total += lightCalc( light1, position, bNormal);
            total += lightCalc( light2, position, bNormal);
            total += lightCalc( light3, position, bNormal);
            color *= vec4(total,  1);

            if (useShadow)
            {
                float cosAngle = dot(normalize(normal), -normalize(shadow0.lightDirection));
                bool facingLight = (cosAngle > 0.01);
                vec3 shadowCoord = (shadowPosition0.xyz + 1.0)/2.0;
                float closestDistanceToLight = texture(shadow0.depthTextureSampler, shadowCoord.xy).r;
                float fragmentDistanceToLight = clamp(shadowCoord.z, 0, 1);
                bool inShadow = (fragmentDistanceToLight > closestDistanceToLight + shadow0.bias);

                if(facingLight && inShadow)
                {
                    float s = 1.0 - shadow0.strength;
                    color *= vec4(s, s, s,1);
                }
            }
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
        self.add_uniform(DataType.vec3, "viewPosition", [0, 0, 0])
        self.add_uniform(DataType.float, "specularStrength", 1)
        self.add_uniform(DataType.float, "shininess", 32)

        if texture is None:
            self.add_uniform(DataType.bool, "useTexture", False)
        else:
            self.add_uniform(DataType.bool, "useTexture", True)
            self.add_uniform(
                DataType.sampler2D, "textureSampler", [texture.texture_ref, 1]
            )

        if bump_texture is None:
            self.add_uniform(DataType.bool, "useBumpTexture", False)
        else:
            self.add_uniform(DataType.bool, "useBumpTexture", True)
            self.add_uniform(
                DataType.sampler2D, "bumpTextureSampler", [bump_texture.texture_ref, 2]
            )
            self.add_uniform(DataType.float, "bumpStrength", 1.0)

        if not use_shadow:
            self.add_uniform(DataType.bool, "useShadow", False)
        else:
            self.add_uniform(DataType.bool, "useShadow", True)
            self.add_uniform(DataType.shadow, "shadow0", None)

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
