import glfw


class SharedContext:
    def __init__(self, state) -> None:
        self.state = state
        if state.window is None:
            raise Exception("[SharedContext] Could not retrieve window from state")

        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        self.window = glfw.create_window(1, 1, "Shared Context", None, state.window)
        if self.window is None:
            raise Exception("[SharedContext] Failed to initialize GLFW window")

        glfw.make_context_current(self.window)

        while state.alive:
            self.step()

        glfw.destroy_window(self.window)

    def step(self):
        print(self.state.frame)
