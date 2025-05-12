{ pkgs ? import <nixpkgs> { } }:

with pkgs;

mkShell rec {
    buildInputs = [
        python312
        python312Packages.pyopengl
        python312Packages.pyopengl-accelerate
        python312Packages.glfw
        python312Packages.pyglm
        python312Packages.numpy
        python312Packages.pillow
        python312Packages.noise
    ];
    LD_LIBRARY_PATH = lib.makeLibraryPath buildInputs;
}
