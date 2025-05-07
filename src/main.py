from core.window import Window
from core.asset_manager import AssetManager

# TODO: use glm
# TODO: logging
# TODO: organize and refactor code
# TODO: update viewport on resize
# TODO: load shaders like assets instead of hardcoding them

if __name__ == "__main__":
    window: Window = Window()
    asset_manager: AssetManager = AssetManager(window.state)
    asset_manager.load_assets()
    window.start_mainloop()

