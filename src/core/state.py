from typing import Any

class State:
    def __init__(self, window: Any) -> None:
        self.frame: int = 0
        self.window: Any = window
        self.alive: bool = True
        self.shared_context_alive: bool = False

    def on_drawcall(self) -> None:
        self.frame += 1

    def on_close(self) -> None:
        self.alive = False

