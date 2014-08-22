#!/usr/bin/python2.7
# Author Ben Everson
# Inspired by citibike-rebalancing.herokuapp.com

import requests
import time
from time import sleep, time, strftime
import datetime
import csv
from sched import scheduler

STATIONS_ENDPOINT = 'http://citibikenyc.com/stations/json'
s = scheduler(time, sleep)

def run_periodically(start, end, interval, func):
    event_time = start
    while event_time < end:
        s.enterabs(event_time, 0, func, ())
        event_time += interval
    s.run()

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

def write_stations(): # write the stations list to a csv file, and append the current date and time
    # get the stations 
    _stations = get_stations()
    # get the date and time
    _thetime = strftime('%Y-%m-%d %H_%M_%S')
    # log the current time
    print "saving file: " + _thetime 
    # append to the stations list
    _stations.append([_thetime])
    # write it all to a file
    _filename = "datafiles/"+ _thetime + ".csv"
    _file = open(_filename, 'wb')
    _writer = csv.writer(_file, quoting=csv.QUOTE_ALL)
    for item in _stations:
        _writer.writerow(item)

# scrape the json data once every 5 minutes (300sec) for 10 hours, starting 30sec from now
run_periodically(time()+10, time()+(10*60*60), 300, write_stations)