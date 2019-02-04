from tkinter import Tk
from view import View

class MainApplication():

    def __init__(self, parent):
        parent.title("ImageResizer")
        self.view = View(parent)

        self.view.init_grid_config()
        self.view.init_canvas()
        self.view.init_components()

        self.view.update_image()
        

if __name__ == "__main__":
    root = Tk()
    # root.resizable(False, False) #disable resizing
    MainApplication(root)
    root.mainloop()