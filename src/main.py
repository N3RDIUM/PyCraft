from core.window import Window
from core.asset_manager import AssetManager
from terrain.chunk import Chunk
from player import Player
import threading
import time

def gen_chunks(dst, state):
    for x in range(-dst, dst + 1):
        for y in range(-dst, dst + 1):
            time.sleep(1)
            Chunk([x, 0, y], state)

if __name__ == "__main__":
    window: Window = Window()
    asset_manager: AssetManager = AssetManager(window.state)
    asset_manager.load_assets()
    thread = threading.Thread(target=lambda: gen_chunks(2, window.state))
    player = Player(window.state)
    window.start_mainloop()
