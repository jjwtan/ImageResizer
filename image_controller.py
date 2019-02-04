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
        self.tk_image = ImageTk.PhotoImage(pil_image)
        return self.tk_image

    def resize_image(self, width, height):
        self.thumnail = self.pil_original_image.copy()
        if width > MAX_IMAGE_THUMBNAIL_WIDTH or height > MAX_IMAGE_THUMBNAIL_HEIGHT:
            return self.tk_image
        else:
            return ImageTk.PhotoImage(self.pil_image_thumnail.resize((width, height), Image.ANTIALIAS))

    def save_image(self, width, height):
        self.pil_image_resized = self.pil_original_image.resize((width, height), Image.ANTIALIAS)
        print("file {}-{}x{}.{} saved".format(os.path.splitext(self.pil_original_image.filename)[0],width,height, self.pil_original_image.format.lower()))
        self.pil_image_resized.save("{}-{}x{}.{}".format(os.path.splitext(self.pil_original_image.filename)[0],width,height, self.pil_original_image.format.lower()),quality=95)

    def get_pil_image(self, file_path):
        print("Opening file {}".format(file_path))
        self.pil_original_image = Image.open(file_path)
        self.pil_image = self.pil_original_image.copy() # keep original image for resizing
        self.ratio=float(self.pil_original_image.height)/self.pil_original_image.width
        self.pil_image.thumbnail((MAX_IMAGE_THUMBNAIL_HEIGHT,MAX_IMAGE_THUMBNAIL_WIDTH), Image.ANTIALIAS) # resize image
        self.pil_image_thumnail = self.pil_image.copy() # keep original image for resizing
        return self.pil_image

    def get_blank_tk_image(self):
        return ImageTk.PhotoImage(Image.new('RGB', (0,0)))

    def get_actual_image_res(self):
        return self.pil_original_image.width, self.pil_original_image.height
