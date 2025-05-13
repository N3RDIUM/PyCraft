import threading
import time
from typing import Any
from .state import State

import glfw


class SharedContext:
    def __init__(self, state: State) -> None:
        self.state: State = state
        if state.window is None:
            raise Exception(
                "[core.shared_context.SharedContext] Could not retrieve window from state"
            )
        self.parent = state.window
        self.thread: threading.Thread | None = None
        self.window: Any | None = None

    def start_thread(self) -> None:
        if self.thread is not None:
            raise Exception(
                "[core.shared_context.SharedContext] Tried to start thread multiple times"
            )
        self.thread = threading.Thread(
            target=self.start,
        )
        self.thread.start()

    def start(self) -> None:
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        self.window = glfw.create_window(
            1, 1, "Shared Context", None, self.parent.window
        )
        if self.window is None:
            raise Exception(
                "[core.shared_context.SharedContext] Failed to initialize GLFW window"
            )
        self.state.shared_context_alive = True

        glfw.make_context_current(self.window)

        while self.state.alive:
            self.step()
            time.sleep(1 / 60)
        
        if self.state.world:
            self.state.world.on_close()
        if self.state.mesh_handler:
            self.state.mesh_handler.on_close()

        glfw.destroy_window(self.window)
        self.state.shared_context_alive = False

    def step(self) -> None:
        if self.state.world:
            self.state.world.update()

        if self.state.mesh_handler:
            self.state.mesh_handler.update()

        glfw.swap_buffers(self.window)
        glfw.poll_events()
