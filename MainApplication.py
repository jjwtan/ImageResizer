from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import os

class MainApplication():
    WINDOW_MIN_HEIGHT = 320
    WINDOW_MIN_WIDTH = 620

    def __init__(self, parent):
        parent.title("Image Resizer")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        parent.grid_rowconfigure(3, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        parent.grid_columnconfigure(3, weight=1)
        parent.geometry("{}x{}+20+20".format(self.WINDOW_MIN_WIDTH, self.WINDOW_MIN_HEIGHT))

        # build canvas
        self.canvas = Canvas(parent, width=620, height=200, borderwidth=2)
        self.canvas.grid(row=0, column=0, columnspan=4)
        self.tk_image = ImageTk.PhotoImage(Image.new('RGB', (0,0)))
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)

        self.width_label = Label(parent, text="Width")
        self.width_label.grid(row=1, column=0, sticky=NSEW)
        self.height_label = Label(parent, text="Height")
        self.height_label.grid(row=1, column=2, sticky=NSEW)

        self.width_slider = Scale(parent, from_=100, to=3000, orient=HORIZONTAL, length=260, resolution=10, command=self.update_height_slider)
        self.width_slider.grid(row=2, column=0, columnspan=2)
        self.height_slider = Scale(parent, from_=100, to=3000, orient=HORIZONTAL, length=260, resolution=10, command=self.update_width_slider)
        self.height_slider.grid(row=2, column=2, columnspan=2)

        self.open_button = Button(parent, text="Open", command= lambda: self.update_image(parent))
        self.open_button.grid(row=3, column=0, sticky=NSEW)
        self.open_button = Button(parent, text="Save", command=self.save_image)
        self.open_button.grid(row=3, column=1, columnspan=2, sticky=NSEW)
        self.open_button = Button(parent, text="Reset", command=self.reset_sliders)
        self.open_button.grid(row=3, column=3, sticky=NSEW)

        self.update_image(parent)

    def reset_sliders(self):
        self.width_slider.set(self.actual_width)
        self.height_slider.set(self.actual_height)

    def save_image(self):
        print("saving image of dimension: {}x{}".format(self.width_slider.get(),self.height_slider.get()))
        self.pil_image_resized = self.pil_image.resize((self.width_slider.get(), self.height_slider.get()), Image.ANTIALIAS)
        print("file {}-{}x{}.{} saved".format(os.path.splitext(self.pil_image.filename)[0],self.width_slider.get(),self.height_slider.get(), self.pil_image.format.lower()))
        self.pil_image_resized.save("{}-{}x{}.{}".format(os.path.splitext(self.pil_image.filename)[0],self.width_slider.get(),self.height_slider.get(), self.pil_image.format.lower()))


    def update_image(self, parent):
        self.open_file()
        if self.file_name:
            self.convert_image()
            self.update_window_size(parent)
            self.width_slider.set(self.actual_width)
            self.height_slider.set(self.actual_height)
            self.canvas.config(width=self.pil_image.width, height=self.pil_image.height)
            self.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)

    def open_file(self):
        self.file_name = filedialog.askopenfilename(title = "Select file",filetypes = (("jpeg files","*.jpg *.png"),("all files","*.*")))

    def convert_image(self):
        self.get_pil_image()
        self.tk_image = ImageTk.PhotoImage(self.pil_image)

    def get_pil_image(self):
        print("Opening file {}".format(self.file_name))
        self.pil_image = Image.open(self.file_name)
        self.actual_height=self.pil_image.height
        self.actual_width=self.pil_image.width
        # resize image
        self.pil_image.thumbnail((800,800), Image.ANTIALIAS)

    def update_window_size(self, parent):
        if self.pil_image.width < self.WINDOW_MIN_WIDTH:
            width = self.WINDOW_MIN_WIDTH
        else:
            width = self.pil_image.width + 5
        parent.geometry("{}x{}".format(width, self.pil_image.height+150))

    def update_height_slider(self, value):
        ratio = float(self.actual_height)/self.actual_width
        self.height_slider.set(int(float(value)*ratio))

    def update_width_slider(self, value):
        ratio = float(self.actual_width)/self.actual_height
        self.width_slider.set(int(float(value)*ratio))


if __name__ == "__main__":
    root = Tk()
    root.resizable(False, False)
    MainApplication(root)
    root.mainloop()