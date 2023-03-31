import sys

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QComboBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

from model_data import PandasModel
from model_combobox_delegate import ComboBoxDelegate



class GuiTable(QtWidgets.QWidget):
    def __init__(self, data_path="data.csv", params=None):
        super().__init__()

        # load data and add empty row
        self.data_path = data_path
        data = pd.read_csv(data_path)

        # set model and add it to the layout
        self.table = QTableView()
        self.model = PandasModel(data)
        self.table.setModel(self.model)     
        self.table.setFixedSize(params.table["size"][0], params.table["size"][1])  

        
        # create empty row
        empty_row = { col:[""] for col in data.columns }
        empty_row["id"] = data["id"].max() + 1

        # set model for new row and add it to the layout
        self.table_new_row = QTableView()
        self.model_new_row = PandasModel(data=pd.DataFrame(empty_row))
        self.table_new_row.setModel(self.model_new_row)
        self.table_new_row.setFixedSize(params.table_new_row["size"][0], params.table_new_row["size"][1])  

        self.delegate = ComboBoxDelegate(parent=self, data=data)
        self.table.setItemDelegate(self.delegate)
        self.delegate_new_row = ComboBoxDelegate(parent=self, data=data)
        self.table_new_row.setItemDelegate(self.delegate_new_row)


             

        # # add empty row
        # self.model.addRow()

        # parameters
        self._sort_ascending = True
        self._sort_column = "id"
        self._sort_entry = "all"
        self._sort_changed = False

        self.showData()
        
    def getData(self):
        return self.model.getData()
    
    def getSortParams(self):
        return self._sort_column, self._sort_entry, self._sort_ascending
    
    def setSortColumn(self, column):
        # do nothing if column is already selected
        if column == self._sort_column:
            return
        
        # set column used for sorting and reset entry
        self._sort_column = column
        self._sort_entry = "all"
        self._sort_changed = True

    def setSortEntry(self, entry):
        # do nothing if entry are already selected
        if entry == self._sort_entry:
            return
        
        # set entry used for sorting
        self._sort_entry = entry
        self._sort_changed = True

    def setSortAscending(self, ascending):
        # do nothing if ascending is already selected
        if ascending == self._sort_ascending:
            return
        
        # set sorting order
        self._sort_ascending = ascending
        self._sort_changed = True

    def showData(self):

        # print(f"showData: {self._sort_column}, {self._sort_entry}, {self._sort_ascending}")
        
        # sort data in model structure if necessary
        if self._sort_changed:     
            self.model.sort(column=self._sort_column, ascending_order=self._sort_ascending)
            self._sort_changed = False

        # get data
        data = self.model.getData()

        # extract indices of rows to show and to hide
        if self._sort_entry == "all":
            show_idx = data.index.tolist()
            hide_idx = []
        else:
            show_idx = data[data[self._sort_column]==self._sort_entry].index.tolist()
            hide_idx = data[data[self._sort_column]!=self._sort_entry].index.tolist()

        print(f"data: {data}")
        print(f"show_idx: {show_idx}")

        # show and hide all rows
        for idx in show_idx: # TODO: optimize for loop
            self.table.showRow(idx)
        for idx in hide_idx:
            self.table.hideRow(idx)
        

    def saveData(self):
        data = self.model.getData().copy(deep=True)
        data = data[pd.to_numeric(data['latitude'], errors='coerce').notnull()]
        data = data[pd.to_numeric(data['longitude'], errors='coerce').notnull()]
        data = data[data["region"].str.len() > 0]
        data = data[data["crack"].str.len() > 0]
        data = data[data["route"].str.len() > 0]

        data.to_csv('data.csv', index=False)



    def addCoords(self, coords):
        print("addCoords")
        data = self.model.getData()
        data_new_row = self.model_new_row.getData()

        # set coordinates in table
        row_idx = 0
        col_idx = data_new_row.columns.get_loc("latitude")
        self.model_new_row.setData(index=self.model_new_row.index(row_idx,col_idx), value=coords['latitude'], role=Qt.EditRole)
        col_idx = data_new_row.columns.get_loc("longitude")
        self.model_new_row.setData(index=self.model_new_row.index(row_idx,col_idx), value=coords['longitude'], role=Qt.EditRole)

        # set closest route
        closest_route_idx = self.closestRoute(data, coords)
        closest_route_region = data["region"].iloc[closest_route_idx]
        col_idx = data_new_row.columns.get_loc("region")
        print(f"col index: {col_idx}")
        self.model_new_row.setData(index=self.model.index(row_idx,col_idx), value=closest_route_region, role=Qt.EditRole)
        closest_route_crack = data["crack"].iloc[closest_route_idx]
        col_idx = data_new_row.columns.get_loc("crack")
        self.model_new_row.setData(index=self.model.index(row_idx,col_idx), value=closest_route_crack, role=Qt.EditRole)

        self.table_new_row.showRow(0)

        print(f"col index: {col_idx}")

        print(f"closest route: {closest_route_region} {closest_route_crack}")

    def closestRoute(self, data, coords):
        # convert positional data to numpy array
        x = data[pd.to_numeric(data['longitude'], errors='coerce').notnull()]['longitude'].to_numpy()
        y = data[pd.to_numeric(data['latitude'], errors='coerce').notnull()]['latitude'].to_numpy()

        # determine index of closest route
        dist_squared = (x-np.array(coords['longitude']))**2 + (y-np.array(coords['latitude']))**2
        return dist_squared.argmin()

    def addRoute(self):
        # add new route from model_new_row to model
        data_new_row = self.model_new_row.getData()
        self.model.addRow(new_row=data_new_row)

        # remove row that was added to model
        self.model_new_row.removeRow(row=0)

        # add empty row
        data = self.model.getData()
        empty_row = { col:[""] for col in data.columns }
        empty_row["id"] = data["id"].max() + 1
        self.model_new_row.addRow(new_row=pd.DataFrame(empty_row))

        # update init. values of comboboxes
        self.delegate.updateInitValues(data=self.model.getData())
        self.delegate_new_row.updateInitValues(data=self.model_new_row.getData())





