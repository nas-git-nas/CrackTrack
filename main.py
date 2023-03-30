import folium
import io
import sys
import json
from branca.element import Element
from PyQt5 import QtCore, QtGui, QtWidgets
import jinja2
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
import pandas as pd

from gui_main import GuiMain

def main():

    df = pd.read_csv('data.csv')
    print(df.head())


    app = QtWidgets.QApplication(sys.argv)

    w = GuiMain(df=df)
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()