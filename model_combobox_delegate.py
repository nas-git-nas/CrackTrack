import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QComboBox, QStyledItemDelegate
from PyQt5.QtCore import Qt, QModelIndex, QAbstractTableModel



class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent, data):
        super().__init__(parent)

        self.box_columns = { idx:name for idx, name in enumerate(data.columns.tolist()) 
                             if name in ('grade','ascend','style','protection','stars') }
        self.box_init_values = { name:data[name].to_numpy() for name in self.box_columns.values() }

        self.grade_list = ['','3a','3a+','3b','3b+','3c','3c+','4a','4a+','4b','4b+','4c','4c+',
                            '5a','5a+','5b','5b+','5c','5c+','6a','6a+','6b','6b+','6c','6c+',
                            '7a','7a+','7b','7b+','7c','7c+','8a','8a+','8b','8b+','8c','8c+']
        ascend_list = ['','normal','redpoint','greenpoint','project']
        style_list = ['','single-pitch','multi-pitch','trad','klettersteig','hochtour']
        protection_list = ['','*','**','***','****']
        stars_list = ['','*','**','***','****']
        self.box_lists = {'grade':self.grade_list, 'ascend':ascend_list, 'style':style_list, 
                          'protection':protection_list, 'stars':stars_list}
        
    def updateInitValues(self, data):
        self.box_init_values = { name:data[name].to_numpy() for name in self.box_columns.values() }

    def createEditor(self, parent, option, index):
        if index.column() in self.box_columns.keys():
            column_name = self.box_columns[index.column()]

            combo_box = QComboBox(parent)
            combo_box.addItems(self.box_lists[column_name])

            init_value = self.box_init_values[column_name][index.row()]
            item_idx = 0
            if init_value in self.box_lists[column_name]:
                item_idx = self.box_lists[column_name].index(init_value)
            combo_box.setCurrentIndex(item_idx)
            return combo_box
        
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        if isinstance(editor, QComboBox):
            current_value = index.data(Qt.DisplayRole)
            editor.setCurrentText(current_value)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QComboBox):
            model.setData(index, editor.currentText(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)