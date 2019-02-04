from configurations import WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH

class View(object):
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("ImageResizer")
        self.init_grid_config()
        self.parent.geometry("{}x{}+20+20".format(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT))

    def init_grid_config(self):
        self.parent.grid_rowconfigure(0, weight=2)
        self.parent.grid_rowconfigure(2, weight=1)
        self.parent.grid_rowconfigure(3, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_columnconfigure(2, weight=1)
        self.parent.grid_columnconfigure(3, weight=1)
