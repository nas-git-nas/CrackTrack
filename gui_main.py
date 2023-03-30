import folium
import io
import sys
import json
from branca.element import Element
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel
import jinja2
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView

from gui_map import GuiMap
from gui_info import GuiInfo
from gui_table import GuiTable
from params import Params

class GuiMain(QtWidgets.QWidget):
    def __init__(self, df):
        super().__init__()
        
        self.params = Params()

        self.df = df

        self.setWindowTitle('Folium map in PyQt')
        self.window_width, self.window_height = (1200, 800)
        self.setMinimumSize(self.window_width, self.window_height)
        self.resize(self.params.main["size"][0], self.params.main["size"][1])

        self.gui_map = GuiMap(
            gui_main=self,
            df=df,
            params=self.params,
        )

        # loading image
        pixmap = QtGui.QPixmap('img.jpg')
        self.images = QLabel()
        self.images.setPixmap(pixmap)
        self.images.setFixedSize(self.params.images["size"][0], self.params.images["size"][1])
        




        self.gui_table = GuiTable(
            params=self.params,
        )

        

        # add AddRoute button
        self.button_add_route = QtWidgets.QPushButton('Add Route')
        self.button_add_route.clicked.connect(self.cbButtonAddRoute)
        self.button_add_route.setFixedSize(self.params.button_add_route["size"][0], self.params.button_add_route["size"][1])
        

        # add Save button
        self.button_save = QtWidgets.QPushButton('Save')
        self.button_save.clicked.connect(self.cbButtonSave)
        self.button_save.setFixedSize(self.params.button_save["size"][0], self.params.button_save["size"][1])
        

        # add combobox for sorting
        self.sort_combobox = QtWidgets.QComboBox(self)
        data = self.gui_table.getData()
        for col in data.columns:
            self.sort_combobox.addItem(col)
        self.sort_combobox.activated[str].connect(self.cbComboboxColumn)
        self.sort_combobox.setFixedSize(self.params.sort_combobox["size"][0], self.params.sort_combobox["size"][1])
        

        self.entry_combobox = QtWidgets.QComboBox(self)
        self.entry_combobox.activated[str].connect(self.cbComboboxEntry)
        self.entry_combobox.setFixedSize(self.params.entry_combobox["size"][0], self.params.entry_combobox["size"][1])
        

        self.order_combobox = QtWidgets.QComboBox(self)
        self.order_combobox.addItem("Sorting: ascending")
        self.order_combobox.addItem("Sorting: descending")
        self.order_combobox.activated[str].connect(self.cbComboboxOrder)
        self.order_combobox.setFixedSize(self.params.order_combobox["size"][0], self.params.order_combobox["size"][1])

        # add left button
        self.button_left = QtWidgets.QPushButton('<-')
        # self.button_add_route.clicked.connect(self.cbButtonAddRoute)
        # self.button_add_route.setFixedSize(self.params.button_add_route["size"][0], self.params.button_add_route["size"][1])

        # add right button
        self.button_right = QtWidgets.QPushButton('->')
        # self.button_add_route.clicked.connect(self.cbButtonAddRoute)
        # self.button_add_route.setFixedSize(self.params.button_add_route["size"][0], self.params.button_add_route["size"][1])
        
        # create layout
        self._initLayout()

    def _initLayout(self):
         # create data button layout
        data_button_layout = QtWidgets.QHBoxLayout()
        data_button_layout.addWidget(self.button_add_route)
        data_button_layout.addWidget(self.button_save)
        data_button_layout.addWidget(self.sort_combobox)
        data_button_layout.addWidget(self.entry_combobox)
        data_button_layout.addWidget(self.order_combobox)

        # create map layout
        map_layout = QtWidgets.QVBoxLayout()
        map_layout.addWidget(self.gui_map.webView)
        map_layout.addLayout(data_button_layout)

        # create img button layout
        img_button_layout = QtWidgets.QHBoxLayout()
        img_button_layout.addWidget(self.button_left)
        img_button_layout.addWidget(self.button_right)

        # create img layout
        img_layout = QtWidgets.QVBoxLayout()
        img_layout.addWidget(self.images)
        img_layout.addLayout(img_button_layout)

        # create upper layout
        upper_layout = QtWidgets.QHBoxLayout()
        upper_layout.addLayout(map_layout)
        upper_layout.addLayout(img_layout)

        # create  layout
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addWidget(self.gui_table.table)
        layout.addWidget(self.gui_table.table_new_row)
        self.setLayout(layout)  

    def cbComboboxColumn(self):
        # convert combobox entry to string
        column = str(self.sort_combobox.currentText())
        
        # set sorting parameters and show data
        self.gui_table.setSortColumn(column=column)
        self.gui_table.showData()

        # get unique values of given column
        data = self.gui_table.getData()
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

    def cbButtonAddRoute(self):
        self.gui_table.addRoute()

    def cbButtonSave(self):
        self.gui_table.saveData()




