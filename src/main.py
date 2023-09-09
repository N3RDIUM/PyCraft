import logging
logging.basicConfig(format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
logging.getLogger(__name__).setLevel(logging.DEBUG)

from core.window import Window

if __name__ == "__main__":
    window = Window()
    window.mainloop()