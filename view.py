from tkinter import *
from tkinter import ttk, filedialog
from image_controller import ImageController
from configurations import *

class View(object):
    def __init__(self, parent):
        self.parent = parent
        self.controller = ImageController(self)
        self.parent.geometry("{}x{}+20+20".format(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT))

    def init_grid_config(self):
        self.parent.grid_rowconfigure(0, weight=2)
        self.parent.grid_rowconfigure(2, weight=1)
        self.parent.grid_rowconfigure(3, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_columnconfigure(2, weight=1)
        self.parent.grid_columnconfigure(3, weight=1)

    def init_components(self):
        self.width_label = Label(self.parent, text="Width")
        self.height_label = Label(self.parent, text="Height")
        
        self.width_slider = Scale(self.parent, from_=DEFAULT_SLIDER_MIN, to=DEFAULT_SLIDER_MAX, orient=HORIZONTAL, length=260, resolution=10, command=self.update_height_slider)
        self.height_slider = Scale(self.parent, from_=DEFAULT_SLIDER_MIN, to=DEFAULT_SLIDER_MAX, orient=HORIZONTAL, length=260, resolution=10, command=self.update_width_slider)
        
        self.open_button = ttk.Button(self.parent, text="Open", command= lambda: self.update_image())
        self.save_button = ttk.Button(self.parent, text="Save", command=self.save_image)
        self.reset_button = ttk.Button(self.parent, text="Reset", command=self.reset_sliders)

        self.height_label.grid(row=1, column=2, sticky=NSEW)
        self.width_label.grid(row=1, column=0, sticky=NSEW)
        self.width_slider.grid(row=2, column=0, columnspan=2)
        self.height_slider.grid(row=2, column=2, columnspan=2)
        self.open_button.grid(row=3, column=0, sticky=NSEW)
        self.save_button.grid(row=3, column=1, columnspan=2, sticky=NSEW)
        self.reset_button.grid(row=3, column=3, sticky=NSEW)

    def init_canvas(self):
        # build inital canvas
        self.canvas = Canvas(self.parent, width=INIT_CANVAS_WIDTH, height=INIT_CANVAS_HEIGHT, borderwidth=2)
        self.canvas.grid(row=0, column=0, columnspan=4)
        self.tk_image = self.controller.get_blank_tk_image()
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=CENTER, image=self.tk_image)


    def open_file(self):
        self.file_path = filedialog.askopenfilename(title = "Select file",filetypes = (("jpeg files","*.jpg *.png"),("all files","*.*")))

    def reset_sliders(self):
        self.width_slider.set(self.actual_width)
        self.height_slider.set(self.actual_height)

    def save_image(self):
        print("saving image of dimension: {}x{}".format(self.width_slider.get(),self.height_slider.get()))
        self.controller.save_image(self.width_slider.get(), self.height_slider.get())
    
    def update_image(self):
        self.open_file()
        if self.file_path:
            self.tk_image = self.controller.convert_image(self.file_path)
            self.actual_width, self.actual_height = self.controller.get_actual_image_res()
            self.update_window_size()
            self.width_slider.set(self.actual_width)
            self.height_slider.set(self.actual_height)
            min_width, min_height, max_width, max_height = self.controller.cal_slider_values()
            self.set_slider_min_max(self.width_slider, min_width, max_width)
            self.set_slider_min_max(self.height_slider, min_height, max_height)
            self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())
            self.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)
            self.canvas.coords(self.image_on_canvas, (self.tk_image.width()/2, self.tk_image.height()/2))

    def update_thumbnail_image(self, tkImage):
        self.canvas.itemconfig(self.image_on_canvas, image=tkImage)

    def update_window_size(self):
        if self.tk_image.width() < WINDOW_MIN_WIDTH: # handling for narrow images
            width = WINDOW_MIN_WIDTH
        else:
            width = self.tk_image.width() + 5
        self.parent.geometry("{}x{}".format(width, self.tk_image.height()+150))

    def set_slider_min_max(self, slider, min_, max_):
        slider.config(from_=min_, to=max_)

    def update_height_slider(self, value):
        self.height_slider.set(self.controller.cal_corr_height(value))
        self.tk_image = self.controller.resize_image(self.width_slider.get(), self.height_slider.get())
        self.update_thumbnail_image(self.tk_image)

    def update_width_slider(self, value):
        self.width_slider.set(self.controller.cal_corr_width(value))


    