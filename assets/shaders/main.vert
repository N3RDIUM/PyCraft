#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 vertexUV;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec3 camera;

out vec2 UV;
out float depth;

void main() {
    vec4 worldPos = model * vec4(position, 1.0);
    gl_Position = projection * view * worldPos;
    depth = length(worldPos.xyz - camera);
    UV = vertexUV;
}
