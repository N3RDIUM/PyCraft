from core.window import Window
from core.asset_manager import AssetManager

if __name__ == "__main__":
    window: Window = Window()
    asset_manager: AssetManager = AssetManager(window.state)
    asset_manager.load_assets()
    window.start_mainloop()
