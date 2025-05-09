from core.window import Window
from core.asset_manager import AssetManager
from terrain.chunk import Chunk

if __name__ == "__main__":
    window: Window = Window()
    asset_manager: AssetManager = AssetManager(window.state)
    asset_manager.load_assets()
    chunk: Chunk = Chunk([0, 0, 0], window.state)
    window.start_mainloop()
