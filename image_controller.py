import os
from PIL import Image, ImageTk
from configurations import *

class ImageController(object):
    def __init__(self, view):
        self.view = view

    def cal_corr_height(self, value):
        return int(float(value)*self.ratio)
    
    def cal_corr_width(self, value):
        return int(float(value)/self.ratio)

    def cal_slider_values(self):
        self.min_corr_height = self.min_corr_width = DEFAULT_SLIDER_MIN
        self.max_corr_height = self.max_corr_width = DEFAULT_SLIDER_MAX
        if self.ratio > 1:
            self.min_corr_height = int(float(DEFAULT_SLIDER_MIN)*self.ratio)
            self.max_corr_width = int(float(DEFAULT_SLIDER_MAX)/self.ratio)
        else:
            self.max_corr_height = int(float(DEFAULT_SLIDER_MAX)*self.ratio)
            self.min_corr_width = int(float(DEFAULT_SLIDER_MIN)/self.ratio)
        
        return (self.min_corr_width, 
                self.min_corr_height,
                self.max_corr_width, 
                self.max_corr_height)

    def convert_image(self, file_path):
        pil_image = self.get_pil_image(file_path)
        return ImageTk.PhotoImage(pil_image)

    def save_image(self, width, height):
        self.pil_image_resized = self.pil_image.resize((width, height), Image.ANTIALIAS)
        print("file {}-{}x{}.{} saved".format(os.path.splitext(self.pil_image.filename)[0],width,height, self.pil_image.format.lower()))
        self.pil_image_resized.save("{}-{}x{}.{}".format(os.path.splitext(self.pil_image.filename)[0],width,height, self.pil_image.format.lower()),quality=95)

    def get_pil_image(self, file_path):
        print("Opening file {}".format(file_path))
        self.pil_image = Image.open(file_path)
        self.actual_height=self.pil_image.height
        self.actual_width=self.pil_image.width
        self.ratio=float(self.actual_height)/self.actual_width
        self.pil_image.thumbnail((MAX_IMAGE_THUMBNAIL_HEIGHT,MAX_IMAGE_THUMBNAIL_WIDTH), Image.ANTIALIAS) # resize image
        return self.pil_image

    def get_blank_tk_image(self):
        return ImageTk.PhotoImage(Image.new('RGB', (0,0)))

    def get_actual_image_res(self):
        return self.actual_width, self.actual_height
