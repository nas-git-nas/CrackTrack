import folium
import io
import sys
import json
from branca.element import Element
from PyQt5 import QtCore, QtGui, QtWidgets
import jinja2
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView



class GuiInfo(QtWidgets.QWidget):
    def __init__(self, layout, df):
        super().__init__()

        #### CEATE SELECT  BUTTON
        self.button_select_point = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(10)
        self.button_select_point.setFont(font)      
        
        self.button_select_point.setGeometry(QtCore.QRect(100,20,200,50))
        self.button_select_point.setText("Select one point")     
        self.button_select_point.clicked.connect(self.clicked_button_select_point)

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.button_select_point)
        layout.addWidget(self.label)

        self.createTable(df=df)
        layout.addWidget(self.tableWidget)

    def createTable(self, df):
        self.tableWidget = QTableWidget()
  
        # row and column count
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])  

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.tableWidget.setItem(i,j, QTableWidgetItem("---"))
   
        #Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def clicked_button_select_point(self):
        print("Clicked")

    def setCoords(self, coords):      
        lat = coords['lat']
        lng = coords['lng']
        coords =  f"latitude: {lat} longitude: {lng}"
        self.label.setText(coords)

    def showInfo(self, df, id):

        # convert string to int
        id = int(id)

        data = df.loc[df['id'] == int(id)]
        

        crack = df[df["id"]==id]["crack"].values[0]

        print(df[df["crack"]==crack].iloc[0,0])

        self.tableWidget.setRowCount(df[df["crack"]==crack].shape[0])

        for i in range(df[df["crack"]==crack].shape[0]):
            for j in range(df[df["crack"]==crack].shape[1]):
                self.tableWidget.setItem(i,j, QTableWidgetItem(str(df[df["crack"]==crack].iloc[i,j])))

        






