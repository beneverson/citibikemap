#!/usr/bin/python2.7
# Author Ben Everson
# Inspired by citibike-rebalancing.herokuapp.com

import requests
import time

STATIONS_ENDPOINT = 'http://citibikenyc.com/stations/json'

def get_stations():
    """Returns a list where each element of that list is a station
    retreived from the endpoint passed in above"""
    stations = []
    _stations = requests.get(STATIONS_ENDPOINT).json()
    
    for _station in _stations['stationBeanList']:
        if _station['statusKey'] == 1:
            stations.append([_station['stationName'], _station['id'],
                             _station['availableDocks'], _station['totalDocks'],
                             _station['latitude'], _station['longitude']])

    return stations

st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print (st)