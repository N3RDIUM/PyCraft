from core.window import Window
from core.asset_manager import AssetManager
from terrain.chunk import Chunk
from player import Player

if __name__ == "__main__":
    window: Window = Window()
    asset_manager: AssetManager = AssetManager(window.state)
    asset_manager.load_assets()
    chunks = []
    
    dst = 2
    for x in range(-dst, dst + 1):
        for y in range(-dst, dst + 1):
            chunk: Chunk = Chunk([x, 0, y], window.state)
            chunks.append(chunk)
    
    player = Player(window.state)
    window.start_mainloop()
