import folium
import io
import sys
import json
from branca.element import Element
from PyQt5 import QtCore, QtGui, QtWidgets
import jinja2
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView

from gui_map import GuiMap
from gui_info import GuiInfo
from gui_table import GuiTable

class GuiMain(QtWidgets.QWidget):
    def __init__(self, df):
        super().__init__()

        self.df = df

        self.setWindowTitle('Folium map in PyQt')
        self.window_width, self.window_height = (1200, 800)
        self.setMinimumSize(self.window_width, self.window_height)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.gui_map = GuiMap(
            gui_main=self,
            layout=layout,
            df=df,
        )

        self.gui_table = GuiTable(
            layout=layout,
        )

        # add AddRoute button
        self.button_add_route = QtWidgets.QPushButton('Add Route')
        self.button_add_route.clicked.connect(self.cbButtonAddRoute)
        layout.addWidget(self.button_add_route)

        # add Save button
        self.button_save = QtWidgets.QPushButton('Save')
        self.button_save.clicked.connect(self.cbButtonSave)
        layout.addWidget(self.button_save)

        # add combobox for sorting
        self.sort_combobox = QtWidgets.QComboBox(self)
        data = self.gui_table.getData()
        for col in data.columns:
            self.sort_combobox.addItem(col)
        self.sort_combobox.activated[str].connect(self.cbComboboxColumn)
        layout.addWidget(self.sort_combobox)

        self.entry_combobox = QtWidgets.QComboBox(self)
        self.entry_combobox.activated[str].connect(self.cbComboboxEntry)
        layout.addWidget(self.entry_combobox)

        self.order_combobox = QtWidgets.QComboBox(self)
        self.order_combobox.addItem("Sorting: ascending")
        self.order_combobox.addItem("Sorting: descending")
        self.order_combobox.activated[str].connect(self.cbComboboxOrder)
        layout.addWidget(self.order_combobox)

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




