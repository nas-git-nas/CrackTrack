import folium
import io
import sys
import json
from branca.element import Element
from PyQt5 import QtCore, QtGui, QtWidgets
import jinja2

from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView



class GuiMapCbHandler(QWebEnginePage):
    def __init__(self, gui_main):
        super().__init__(gui_main)
        self.gui_main = gui_main            

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        # print(msg) # Check js errors
        if 'coordinates' in msg:
            self.gui_main.cbMap(msg)
        else:
            self.gui_main.cbMarker(msg)