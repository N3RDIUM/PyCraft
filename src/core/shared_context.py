import glfw
import threading
from typing import Any

class SharedContext:
    def __init__(self, state) -> None:
        self.state = state
        if state.window is None:
            raise Exception(
                "[core.shared_context.SharedContext] Could not retrieve window from state"
            )
        self.thread: threading.Thread | None = None
        self.window: Any | None = None
        self.function_queue = []

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
            1, 1, "Shared Context", None, self.state.window.window
        )
        if self.window is None:
            raise Exception(
                "[core.shared_context.SharedContext] Failed to initialize GLFW window"
            )
        self.state.shared_context_alive = True

        glfw.make_context_current(self.window)

        while self.state.alive:
            self.step()

        self.state.mesh_handler.on_close()
        glfw.destroy_window(self.window)
        self.state.shared_context_alive = False

    def schedule_fn(self, func) -> None:
        self.function_queue.append(func)

    def step(self) -> None:
        if len(self.function_queue) > 0:
            fn = self.function_queue.pop(0)
            fn()

        if self.state.mesh_handler:
            self.state.mesh_handler.update()

        glfw.swap_buffers(self.window)
        glfw.poll_events()
