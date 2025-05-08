import glfw
import threading
from typing import Any
from .dynamic_vbo import DynamicVBOHandler

class SharedContext:
    def __init__(self, state) -> None:
        self.state = state
        if state.window is None:
            raise Exception("[core.shared_context.SharedContext] Could not retrieve window from state")
        self.thread: threading.Thread | None = None
        self.window: Any | None = None
        self.function_queue = []
        self.vbo_handlers: dict[str, DynamicVBOHandler] = {}

    def register_vbo_handler(self, handler: DynamicVBOHandler, id: str) -> None:
        self.vbo_handlers[id] = handler

    def unregister_vbo_handler(self, id: str) -> DynamicVBOHandler:
        return self.vbo_handlers.pop(id)
    
    def start_thread(self) -> None:
        if self.thread is not None:
            raise Exception("[core.shared_context.SharedContext] Tried to start thread multiple times")
        self.thread = threading.Thread(
            target = self.start,
        )
        self.thread.start()

    def start(self) -> None:
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        self.window = glfw.create_window(1, 1, "Shared Context", None, self.state.window.window)
        if self.window is None:
            raise Exception("[core.shared_context.SharedContext] Failed to initialize GLFW window")
        self.state.shared_context_alive = True

        glfw.make_context_current(self.window)
        
        while self.state.alive:
            self.step()

        glfw.destroy_window(self.window)
        self.state.shared_context_alive = False

    def schedule_fn(self, func) -> None:
        self.function_queue.append(func)

    def step(self) -> None:
        if len(self.function_queue) > 0:
            fn = self.function_queue.pop(0)
            fn()

        for handler in self.vbo_handlers:
            self.vbo_handlers[handler].update()

        glfw.swap_buffers(self.window)
        glfw.poll_events()

