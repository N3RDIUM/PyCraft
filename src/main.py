from core.window import Window
from core.asset_manager import AssetManager
from player import Player

if __name__ == "__main__":
    window: Window = Window()
    asset_manager: AssetManager = AssetManager(window.state)
    asset_manager.load_assets()
    player = Player(window.state)
    window.start_mainloop()
