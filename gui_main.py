import folium
import io
import sys
import json
from branca.element import Element
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel
import jinja2
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtGui import QPixmap, QResizeEvent

from gui_map import GuiMap
from gui_info import GuiInfo
from gui_table import GuiTable
from params import Params
from gui_images import GuiImages

class GuiMain(QtWidgets.QWidget):
    def __init__(self, df):
        super().__init__()
        
        self.params = Params()
        self.df = df
        
        # add map
        self.gui_map = GuiMap(
            gui_main=self,
            df=df,
            params=self.params,
        )

        # add images
        self.gui_images = GuiImages()

        # add table
        self.gui_table = GuiTable(
            params=self.params,
        )

        # add AddRoute button
        self.button_add_route = QtWidgets.QPushButton('Add Route')
        self.button_add_route.clicked.connect(self.cbButtonAddRoute)

        # add Save button
        self.button_save = QtWidgets.QPushButton('Save')
        self.button_save.clicked.connect(self.cbButtonSave)

        # add combobox for sorting
        self.sort_combobox = QtWidgets.QComboBox(self)
        data = self.gui_table.getData()
        for col in data.columns:
            self.sort_combobox.addItem(col)
        self.sort_combobox.activated[str].connect(self.cbComboboxColumn)

        self.entry_combobox = QtWidgets.QComboBox(self)
        self.entry_combobox.activated[str].connect(self.cbComboboxEntry)
        
        self.order_combobox = QtWidgets.QComboBox(self)
        self.order_combobox.addItem("Sorting: ascending")
        self.order_combobox.addItem("Sorting: descending")
        self.order_combobox.activated[str].connect(self.cbComboboxOrder)

        # add left and right button
        self.button_left = QtWidgets.QPushButton('<-')
        self.button_left.clicked.connect(self.cbButtonLeft)
        self.button_right = QtWidgets.QPushButton('->')
        self.button_right.clicked.connect(self.cbButtonRight)
        
        # create layout
        self._initLayout()

    def _initLayout(self):
        # main layout
        self.setWindowTitle('Crack Track')
        self.setMinimumSize(2400, 1600)

        # create data button layout
        self.button_add_route.setMinimumSize(120, 40)
        self.button_save.setMinimumSize(120, 40)
        self.sort_combobox.setMinimumSize(180, 40)
        self.entry_combobox.setMinimumSize(180, 40)
        self.order_combobox.setMinimumSize(180, 40)
        data_button_layout = QtWidgets.QHBoxLayout()
        data_button_layout.addWidget(self.button_add_route, stretch=1)
        data_button_layout.addWidget(self.button_save, stretch=1)
        data_button_layout.addWidget(self.sort_combobox, stretch=2)
        data_button_layout.addWidget(self.entry_combobox, stretch=2)
        data_button_layout.addWidget(self.order_combobox, stretch=2)

        # create map layout
        self.gui_map.webView.setMinimumSize(1000, 600)
        map_layout = QtWidgets.QVBoxLayout()
        map_layout.addWidget(self.gui_map.webView)
        map_layout.addLayout(data_button_layout)

        # create img button layout
        self.button_left.setMinimumSize(120, 40)
        self.button_right.setMinimumSize(120, 40)
        img_button_layout = QtWidgets.QHBoxLayout()
        img_button_layout.addStretch(3)
        img_button_layout.addWidget(self.button_left, stretch=1)
        img_button_layout.addWidget(self.button_right, stretch=1)
        img_button_layout.addStretch(3)

        # create img layout
        self.gui_images.image_label.setMinimumSize(900, 600)
        img_layout = QtWidgets.QVBoxLayout()
        img_layout.addWidget(self.gui_images.image_label)
        img_layout.addLayout(img_button_layout)

        # create upper layout
        upper_layout = QtWidgets.QHBoxLayout()
        upper_layout.addLayout(map_layout, stretch=3)
        upper_layout.addLayout(img_layout, stretch=2)

        # create  layout
        self.gui_table.table.setMinimumSize(1000, 600)
        self.gui_table.table_new_row.setMinimumSize(1000, 150)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(upper_layout, stretch=12)
        layout.addWidget(self.gui_table.table, stretch=3)
        layout.addWidget(self.gui_table.table_new_row, stretch=1)
        self.setLayout(layout)  

    def cbComboboxColumn(self):
        # convert combobox entry to string
        column = str(self.sort_combobox.currentText())
        
        # set sorting parameters and show data
        self.gui_table.setSortColumn(column=column)
        self.gui_table.showData()

        # update images
        data = self.gui_table.getData()
        sort_column, sort_entry, _ = self.gui_table.getSortParams()
        self.gui_images.updateImages(data=data, sort_column=sort_column, sort_entry=sort_entry)

        # get unique values of given column     
        unique_values = data[column].unique()
        unique_values = unique_values.astype(str).tolist()
        
        # add "all" to unique values
        unique_values.insert(0, "all")

        # update entry_combobox
        self.entry_combobox.clear()
        self.entry_combobox.addItems(unique_values)

    def cbComboboxEntry(self):
        # convert combobox entry to string
        entry = str(self.entry_combobox.currentText())

        # set sorting parameters and show data
        self.gui_table.setSortEntry(entry=entry)
        self.gui_table.showData()

        # update images
        data = self.gui_table.getData()
        sort_column, sort_entry, _ = self.gui_table.getSortParams()
        self.gui_images.updateImages(data=data, sort_column=sort_column, sort_entry=sort_entry)

    def cbComboboxOrder(self):
        # print(str(self.order_combobox.currentText()))

        # convert combobox entry to bool
        ascending_order=False
        if str(self.order_combobox.currentText()) == "Sorting: ascending":
            ascending_order=True
        
        # set sorting parameters and show data
        self.gui_table.setSortAscending(ascending=ascending_order)
        self.gui_table.showData()

    def cbMap(self, msg):
        # convert msg to coordinates
        data = json.loads(msg)
        coords = { "latitude":data['coordinates']['lat'], "longitude":data['coordinates']['lng'] }

        # set coordinates and show data
        self.gui_table.addCoords(coords=coords)
        self.gui_table.showData()

    def cbMarker(self, msg):

        # get data
        data = self.gui_table.getData()

        # convert msg to crack name
        id = int(msg)
        entry = data[data["id"]==id]["crack"].values[0]   

        # set sorting parameters and show data
        self.gui_table.setSortColumn(column="crack")
        self.gui_table.setSortEntry(entry=entry)
        self.gui_table.showData()

        # update images
        data = self.gui_table.getData()
        sort_column, sort_entry, _ = self.gui_table.getSortParams()
        self.gui_images.updateImages(data=data, sort_column=sort_column, sort_entry=sort_entry)

    def cbButtonAddRoute(self):
        self.gui_table.addRoute()

    def cbButtonSave(self):
        self.gui_table.saveData()

    def cbButtonLeft(self):
        self.gui_images.decreaseIdx()

    def cbButtonRight(self):
        self.gui_images.increaseIdx()

    def resizeEvent(self, event: QResizeEvent):
        self.gui_images.set_image_size()
        event.accept()




