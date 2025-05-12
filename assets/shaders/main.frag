#version 330 core

in float depth;
in vec2 UV;

uniform vec3 fogColor;
uniform float fogStart;
uniform float fogEnd;

out vec3 color;
uniform sampler2D myTextureSampler;

void main() {
    float fogFactor = clamp((fogEnd - depth) / (fogEnd - fogStart), 0.0, 1.0);
    color = mix(fogColor, texture( myTextureSampler, UV ).rgb, fogFactor);
}
