import time
from typing import Any


class State:
    def __init__(self, window: Any) -> None:
        self.frame: int = 0
        self.window: Any = window
        self.alive: bool = True
        self.shared_context_alive: bool = False
        self.asset_manager: Any | None = None
        self.mesh_handler: Any | None = None
        self.camera: Any | None = None
        self.player: Any | None = None
        self.world: Any | None = None

        self.last_frame_time: float = time.time()
        self.fps = 0
        self.delta = 0

    def on_drawcall(self) -> None:
        now = time.time()
        self.delta = now - self.last_frame_time
        self.last_frame_time = now

        self.fps = 1 / self.delta

        self.frame += 1
        print(f"\r{self.fps} FPS", end="\t\t")

        if self.delta < 1 / 128:
            time.sleep(1 / 128 - self.delta)

    def on_close(self) -> None:
        self.alive = False
