import numpy as np
import copy
import numbers


from src.gps_converter import GPSConverter
from PyQt5.QtCore import QAbstractTableModel, Qt


class ConvertData():
    def __init__(self, model) -> None:

        # PandasModel class instance
        self.model = model

        # create GPS conversion class instance
        self.gps_converter = GPSConverter()

    def setData(self, index, value):

        print(f"_convertCoords: value: {value}, type of value: {type(value)}")
        print(f"index row: {index.row()}, type {type(index.row())}, index column: {index.column()}")

        print("----------------------------")

        # get column name and function
        col_name = self.model._data.columns[index.column()]
        col_fct = getattr(self, col_name)

        # return dict with changed data: key=index, value=value
        return col_fct(index=index, value=value)        

    def id(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        data_changed[index] = int(value)
        return data_changed

    def region(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        data_changed[index] = str(value)
        return data_changed

    def crack(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        data_changed[index] = str(value)
        return data_changed

    def route(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        data_changed[index] = str(value)
        return data_changed

    def grade(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        data_changed[index] = str(value)
        return data_changed

    def stars(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        data_changed[index] = str(value)
        return data_changed

    def protection(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        data_changed[index] = str(value)
        return data_changed

    def ascend(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        data_changed[index] = str(value) # TODO: change
        return data_changed

    def date(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        data_changed[index] = str(value) # TODO: change
        return data_changed

    def longitude(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        value = float(value)
        data_changed[index] = value

        # get latitude
        latitude = self.model._data["latitude"].iloc[index.row()]

        # if latitiude is already defined convert gloabel coords. into LV03
        if isinstance(latitude, numbers.Number):
            data_changed = self._WGS84toLV03(data_changed=data_changed, latitude=latitude, longitude=value, row=index.row())

        return data_changed
        

    def latitude(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        value = float(value)
        data_changed[index] = value

        # get longitude
        longitude = self.model._data["longitude"].iloc[index.row()]

        # if latitiude is already defined convert gloabel coords. into LV03
        if isinstance(longitude, numbers.Number):
            data_changed = self._WGS84toLV03(data_changed=data_changed, latitude=value, longitude=longitude, row=index.row())

        return data_changed
    
    def east(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        value = float(value)
        data_changed[index] = value

        # get north
        north = self.model._data["north"].iloc[index.row()]

        # if latitiude is already defined convert gloabel coords. into LV03
        if isinstance(north, numbers.Number):
            data_changed = self._LV03toWGS84(data_changed=data_changed, east=value, north=north, row=index.row())

        return data_changed
    
    def north(self, index, value):
        # dict. containing data that will be changed
        data_changed = {}

        # convert str into int
        value = float(value)
        data_changed[index] = value

        # get north
        east = self.model._data["east"].iloc[index.row()]

        # if latitiude is already defined convert gloabel coords. into LV03
        if isinstance(east, numbers.Number):
            data_changed = self._LV03toWGS84(data_changed=data_changed, east=east, north=value, row=index.row())

        return data_changed
    
    def _WGS84toLV03(self, data_changed, latitude, longitude, row):
        # convert gloabel coords. into LV03
        coords_lv03 = self.gps_converter.WGS84toLV03(latitude=latitude, longitude=longitude, ellHeight=0)
        coords_lv03 = np.round(coords_lv03, 1)

        # create index of data location
        index_lv03_east = self.model.index(row, self.model._data.columns.get_loc("east"))
        index_lv03_north = self.model.index(row, self.model._data.columns.get_loc("north"))

        # add data to dict.
        data_changed[index_lv03_east] = coords_lv03[0]
        data_changed[index_lv03_north] = coords_lv03[1]
        return data_changed
    

    def _LV03toWGS84(self, data_changed, east, north, row):
        # convert gloabel coords. into LV03
        coords_wgs84 = self.gps_converter.LV03toWGS84(east=east, north=north, height=0)
        coords_wgs84 = np.round(coords_wgs84, 1)

        # create index of data location
        
        index_wgs84_latitude = self.model.index(row, self.model._data.columns.get_loc("latitude"))
        index_wgs84_longitude = self.model.index(row, self.model._data.columns.get_loc("longitude"))

        # add data to dict.
        data_changed[index_wgs84_latitude] = coords_wgs84[0]
        data_changed[index_wgs84_longitude] = coords_wgs84[1]
        return data_changed