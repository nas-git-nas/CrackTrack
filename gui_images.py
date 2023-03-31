from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtCore import Qt

import os
import numpy as np



class GuiImages(QtWidgets.QWidget):
    def __init__(self) -> None:  
        super().__init__()       
        # create image label
        self.image_label = QLabel()

        # path to image directory
        self.imgs_path = "C://Users//nicol//OneDrive//Documents//Climbing//CrackTrack//imgs"
        self.default_img = "img.jpg"

        # load images and set first image
        self.imgs = [QPixmap(os.path.join(self.imgs_path, self.default_img))]
        self.idx = 0
        self.set_image_size()       

    def set_image_size(self):
        self.imgs[self.idx] = self.imgs[self.idx].scaled(self.image_label.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.image_label.setPixmap(self.imgs[self.idx])

    def updateImages(self, data, sort_column, sort_entry):
        # get image directories
        if sort_entry == "all":
            sorted_data = data
        else:
            sorted_data = data[data[sort_column]==sort_entry]
        img_dirs = sorted_data["imgs"].unique().tolist()

        # load images
        self.imgs = []
        for dir in img_dirs:
            if not isinstance(dir, str):
                continue

            path = os.path.join(self.imgs_path, dir)
            for file in os.listdir(path):
                self.imgs.append(QPixmap(os.path.join(path, file)))

        # if no images are found, use default image
        if len(self.imgs) == 0:
            self.imgs.append(QPixmap(os.path.join(self.imgs_path, self.default_img)))

        # choose random image
        rng = np.random.default_rng()
        self.idx = rng.choice(len(self.imgs))

        # set image
        self.set_image_size()

    def increaseIdx(self):
        self.idx += 1
        if self.idx >= len(self.imgs):
            self.idx = 0
        self.set_image_size()

    def decreaseIdx(self):
        self.idx -= 1
        if self.idx < 0:
            self.idx = len(self.imgs) - 1
        self.set_image_size()
