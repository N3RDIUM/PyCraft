class State:
    def __init__(self) -> None:
        self.frame: int = 0

    def on_drawcall(self) -> None:
        self.frame += 1

