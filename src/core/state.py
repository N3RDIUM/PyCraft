import time
from typing import Any

class State:
    def __init__(self, window: Any) -> None:
        self.frame: int = 0
        self.window: Any = window
        self.alive: bool = True
        self.shared_context_alive: bool = False
        self.asset_manager: Any | None = None
        self.vbo_handler: Any | None = None
        self.camera: Any | None = None

        self.last_frame_time: int = time.time_ns()
        self.fps = 0

    def on_drawcall(self) -> None:
        now = time.time_ns()
        delta = (now - self.last_frame_time)
        self.fps = 1_000_000_000 / delta
        self.last_frame_time = now

        self.frame += 1

    def on_close(self) -> None:
        self.alive = False

