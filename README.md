<p align=center>
    <img src="./assets/voxl_logo.svg" alt="Voxl Logo" />
</p>

# Voxl
Meet Voxl, a highly optimized infinite procedural voxel terrain generating thing in written in Python.

## Features
- Infinite terrain with no bounds in any axis. (yes, no height limit!)
- OpenSimplex-based terrain generation with caves (very wip)
- Terrain is just stone for now, multiple materials coming soon.

## Usage

Install the [Nix](https://nixos.org/) Package Manager:
```bash
$ sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install) --daemon
```

Clone this repo and `cd` into it:
```bash
git clone https://n3rdium/Voxl.git voxl
cd voxl
```

Enter nix shell (this will "install" all deps for you):
```bash
nix-shell
```

Now, to start Voxl, run:
```bash
python src/main.py
```

## Controls
```
Move Forward  : W
Move Left     : A
Move Backward : S
Move Right    : D
Move Up       : space
Move Down     : shift
Sprint        : ctrl

Lock mouse    : L
Unlock mouse  : esc
```

## Screenshots
Coming soon!

## Contributing
Coming soon!


