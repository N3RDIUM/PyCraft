#version 150
uniform struct {
  vec4 position;
  vec3 color;
  vec3 attenuation;
  vec3 spotDirection;
  float spotCosCutoff;
  float spotExponent;
  sampler2DShadow shadowMap;
  mat4 shadowViewMatrix;
} p3d_LightSource[1];
const float M_PI = 3.141592653589793;
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat3 p3d_NormalMatrix;
in vec4 vertex;
in vec3 normal;
in vec2 p3d_MultiTexCoord0;
uniform vec2 texture_scale;
uniform vec2 texture_offset;
out vec2 texcoords;
out vec3 vpos;
out vec3 norm;
out vec4 shad[1];
void main() {
  gl_Position = p3d_ModelViewProjectionMatrix * vertex;
  vpos = vec3(p3d_ModelViewMatrix * vertex);
  norm = normalize(p3d_NormalMatrix * normal);
  shad[0] = p3d_LightSource[0].shadowViewMatrix * vec4(vpos, 1);
  texcoords = (p3d_MultiTexCoord0 * texture_scale) + texture_offset;
}
