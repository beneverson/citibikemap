#!/usr/bin/python2.7
# Author Ben Everson
# Inspired by citibike-rebalancing.herokuapp.com

import requests
from os import listdir
from time import strptime, strftime
import re
import csv

STATIONS_ENDPOINT = 'http://citibikenyc.com/stations/json'
DATAFILES_PATH = 'datafiles/archive/datafiles/'

def get_recent_statuses(num=100):
    # files are stored in the datafiles directory
    filenames = listdir(DATAFILES_PATH) # get a list of all file names in directory
    _filedates = []
    for _fname in filenames: # iterate over all file names, most to least recent
        # check if the file name conforms to the proper convention
        m = re.match('([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2})_([0-9]{2})_([0-9]{2})', _fname)
        if m and len(_filedates) < num: _filedates.append(strptime(m.group(0), '%Y-%m-%d %H_%M_%S')) 
    
    # _mostrecent now holds the 'num' most recent file dates
    _filedates.sort() # sort the list
    _filedates.reverse() # make most recent dates first
    
    # a list to hold the assosciated file names
    _mostrecent = []
    
    for _fd in _filedates:
        # generate the name
        _filename = strftime('%Y-%m-%d %H_%M_%S', _fd) + '.csv'
        #print 'Archiving ' + _filename
        _mostrecent.append(_filename)
    
    # create a dict to hold all of the 'num' most recent data files
    # key will be the timestamp, and value will be the station statuses at that time
    recentstatuses = {}
    # go through all of _mostrecent
    for _recentstations in _mostrecent:
        # open the file
        _recentstationsdata = []
        with open(DATAFILES_PATH + _recentstations, 'Ur') as _f:
            _recentstationsdata = list(rec for rec in csv.reader(_f, delimiter=','))
        # retrieve the timestamp from the file
        _timestamplist = _recentstationsdata.pop()
        _timestamp = _timestamplist[0]
        # append this status to the master list
        recentstatuses[_timestamp] = _recentstationsdata
    
    return recentstatuses
            
    

def get_stations():
    stations = []
    _stations = requests.get(STATIONS_ENDPOINT).json()
    
    for _station in _stations['stationBeanList']:
        if _station['statusKey'] == 1:
            stations.append([_station['stationName'], _station['id'],
                             _station['availableDocks'], _station['totalDocks'],
                             _station['latitude'], _station['longitude']])

    return stations

def num_free_bikes(availableDocks, totalDocks):
    # return the number of free bikes from the given data
    return totalDocks - availableDocks
