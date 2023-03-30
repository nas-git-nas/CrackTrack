import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

from convert_data import ConvertData


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self.convert_data = ConvertData(model=self)

        

    def getData(self):
        return self._data.copy(deep=True)

    def rowCount(self, index=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.EditRole:

            # # convert coordinates if any coordinate column is edited
            # if index.column() == self._longitude_idx or index.column() == self._latitude_idx \
            #     or index.column() == self._north_idx or index.column() == self._east_idx:
            #     self._convertCoords(index=index, value=value)
            #     value = float(value) # TODO: find better solution, data structure

            data_changed = self.convert_data.setData(index=index, value=value)

            print(f"changed data: {data_changed}")

            for i, v in data_changed.items():
                self._data.iloc[i.row(), i.column()] = v
                self.dataChanged.emit(i, i, (Qt.DisplayRole, Qt.EditRole))

            return True
        return False

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
    
    def addRow(self, new_row):

        row = len(self._data) + 1
        self.rowsAboutToBeInserted.emit(QtCore.QModelIndex(), row, row)

        # add new row to data
        self._data = pd.concat([self._data, new_row], axis=0, ignore_index=True)

        self.rowsInserted.emit(QtCore.QModelIndex(), row, row)

    def removeRow(self, row):

        self.rowsAboutToBeRemoved.emit(QtCore.QModelIndex(), row, row)

        # remove row from data
        self._data.drop(index=row, inplace=True)

        self.rowsRemoved.emit(QtCore.QModelIndex(), row, row)

    def sort(self, column, ascending_order):
        """Sort table by given column number.
        """
        try:
            self.layoutAboutToBeChanged.emit()
            self._data = self._data.sort_values(column, ascending=ascending_order, ignore_index=True)
            self.layoutChanged.emit()
        except Exception as e:
            print(e)
    
    
        
    


class ModelData(PandasModel):
    def __init__(self, data):
        super().__init__(data=data)


    

class ModelNewRow(PandasModel):
    def __init__(self, data):
        # create empty row
        empty_row = { col:[""] for col in data.columns }
        empty_row["id"] = data["id"].max() + 1

        # init pandas model
        super().__init__(data=pd.DataFrame(empty_row))