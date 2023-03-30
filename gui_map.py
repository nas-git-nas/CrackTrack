import folium
import io
import sys
import json
from branca.element import Element
from PyQt5 import QtCore, QtGui, QtWidgets
import jinja2
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView

from gui_map_cb_handler import GuiMapCbHandler

class GuiMap(QtWidgets.QWidget):
    def __init__(self, gui_main, df, params):
        super().__init__()

        coordinate = (47.548, 7.591)
        m = folium.Map(
                tiles='Stamen Terrain',
                zoom_start=10,
                location=coordinate
            )

        self.addMarkers(map_object=m, df=df)


        self.addMarkerEvent(map_object=m)

        #Add Custom JS to folium map
        m = self.add_customjs(m)
        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        self.webView = QWebEngineView() # start web engine
        page = GuiMapCbHandler(gui_main=gui_main)
        self.webView.setPage(page)
        self.webView.setHtml(data.getvalue().decode()) #give html of folium map to webengine
        

    def addMarkers(self, map_object, df):

        tooltip = "Click me!"

        for crack in df["crack"].unique():
            print(df[df["crack"]==crack]["id"].values[0])

            latitudes = df[df["crack"]==crack]["latitude"].mean()
            longitudes = df[df["crack"]==crack]["longitude"].mean()
        
            # folium.Marker(
            #     [47.2912, 7.42338], popup = f'<input type="text" value="{47.2912}, {7.42338}" id="myInput"><button onclick="myFunction()">Copy location</button>', tooltip=tooltip
            # ).add_to(map_object)

            folium.Marker(
                [latitudes, longitudes],
                popup = f'<button onclick="myFunction({df[df["crack"]==crack]["id"].values[0]})">{df[df["crack"]==crack]["crack"].values[0]}</button>', 
                tooltip=f'{df[df["crack"]==crack]["crack"].values[0]}',
            ).add_to(map_object)

    
    def addMarkerEvent(self, map_object):
        el = folium.MacroElement().add_to(map_object)
        el._template = jinja2.Template("""
            {% macro script(this, kwargs) %}
            function myFunction(id) {
                console.log(id);
            }
            {% endmacro %}
        """)
        # el._template = jinja2.Template("""
        #     {% macro script(this, kwargs) %}
        #     function myFunction() {
        #         console.log(data);
        #     }
        #     {% endmacro %}
        # """)

    def add_customjs(self, map_object):
        my_js = f"""{map_object.get_name()}.on("click",
                 function (e) {{
                    var data = `{{"coordinates": ${{JSON.stringify(e.latlng)}}}}`;
                    console.log(data)}});"""

        e = Element(my_js)
        html = map_object.get_root()
        html.script.get_root().render()
        # Insert new element or custom JS
        html.script._children[e.get_name()] = e

        return map_object