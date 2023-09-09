import threading
import logging

import glfw

# Config the logger
logger = logging.getLogger("PyCraft")
file_handler = logging.FileHandler("pycraft.log")
file_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

class Window:
    def __init__(self):
        """
        Init GLFW, and create a new window
        """
        logger.log(logging.DEBUG, "[core/window] Initializing GLFW")
        if not glfw.init():
            logger.log(logging.FATAL, "[core/window] GLFW failed to initialize")
            raise Exception("GLFW failed to initialize")
        
        self.context_event = threading.Event()
        self.shared_context_scheduled = []
        self.drawcall_scheduled = []
        
        logger.log(logging.DEBUG, "[core/window] Creating window")
        self.window = glfw.create_window(800, 600, "PyCraft", None, None)
        if not self.window:
            logger.log(logging.FATAL, "[core/window] Failed to create window")
            glfw.terminate()
            raise Exception("Failed to create window")
        glfw.make_context_current(self.window)
        
        logger.log(logging.DEBUG, "[core/window] Creating shared context")
        self.thread = threading.Thread(target=self.shared_context)
        self.thread.start()
        self.context_event.wait()
        
    def shared_context(self):
        """
        Make another window, and share the context with the main window
        Then we can use this window to process the scheduled stuff.
        """
        logger.log(logging.DEBUG, "[core/window: shared_context] Initializing shared context")
        if not glfw.init():
            logger.log(logging.FATAL, "[core/window: shared_context] GLFW failed to initialize in shared context")
            raise logger("GLFW failed to initialize in shared context")
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        new_window = glfw.create_window(500, 500, "Shared Context", None, self.window)
        glfw.make_context_current(new_window)
        self.context_event.set()
        logger.log(logging.DEBUG, "[core/window: shared_context] Shared context initialized")
        
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            for obj in self.shared_context_scheduled:
                obj.shared_context()
            glfw.swap_buffers(self.window)
        
        logger.log(logging.DEBUG, "[core/window: shared_context] Shared context terminated")
        glfw.destroy_window(new_window)
        glfw.terminate()
        
    def schedule_shared_context(self, obj):
        """
        Schedule an object to be processed in the shared context
        """
        self.shared_context_scheduled.append(obj)
        
    def mainloop(self):
        """
        The main loop of the window
        """
        logger.log(logging.DEBUG, "[core/window] Main loop started")
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            for obj in self.drawcall_scheduled:
                obj.drawcall()
            glfw.swap_buffers(self.window)
            
    def schedule_drawcall(self, obj):
        """
        Schedule an object to be processed in the main loop
        """
        self.drawcall_scheduled.append(obj)