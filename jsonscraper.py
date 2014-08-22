#!/usr/bin/python2.7
# Author Ben Everson
# Inspired by citibike-rebalancing.herokuapp.com

import requests
import time
from time import sleep, time, strftime, strptime
import datetime
import csv
from sched import scheduler
import tarfile
from os import listdir, remove
import re

STATIONS_ENDPOINT = 'http://citibikenyc.com/stations/json'
DATAFILES_PATH = 'datafiles/'
ARCHIVE_PATH = 'datafiles/archive/'

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

def archive_old_stations(to_keep=20, min_archive_size=100):
    # get all the file names in the directory
    # files are stored in the datafiles directory
    filenames = listdir(DATAFILES_PATH)
    # create a list of all the dates of all files in the folder 
    _filedates = [] 
    for _fname in filenames: # iterate over all file names, most to least recent
        # check if the file name conforms to the proper convention
        m = re.match('([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2})_([0-9]{2})_([0-9]{2})', _fname)
        if m: 
            _filedates.append(strptime(m.group(0), '%Y-%m-%d %H_%M_%S')) 
    # return if we don't have enough files in the directory
    if len(_filedates) < (to_keep + min_archive_size):
        print str(len(_filedates)) + ' Files ..'
        return
    else:
        # print 'Now archiving old files...'
        _filedates.sort() # sort the list
        _filedates.reverse() # make most recent dates first
        _filedates_keep = _filedates[:to_keep-1] # the keep list
        _filedates_archive = _filedates[to_keep:] # the archive list
        archivename = ARCHIVE_PATH + strftime('%Y-%m-%d-%H_%M_%S') + '.tar.gz' # generate the archive name
        tar = tarfile.open(archivename, 'w:gz')
        for _fd in _filedates_archive:
            # generate the name
            _filename = DATAFILES_PATH + strftime('%Y-%m-%d %H_%M_%S', _fd) + '.csv'
            #print 'Archiving ' + _filename
            tar.add(_filename)
        tar.close()
        for _fd in _filedates_archive: # delete the original (uncompressed) files
            # generate the name
            _filename = DATAFILES_PATH + strftime('%Y-%m-%d %H_%M_%S', _fd) + '.csv'
            #print 'Deleting ' + _filename
            remove(_filename) 
        
        
        

def write_stations(): # write the stations list to a csv file, and append the current date and time
    # first archive old files
    archive_old_stations()
    # get the stations 
    _stations = get_stations()
    # get the date and time
    _thetime = strftime('%Y-%m-%d %H_%M_%S')
    # log the current time
    # print "saving file: " + _thetime 
    # append to the stations list
    _stations.append([_thetime])
    # write it all to a file
    _filename = "datafiles/"+ _thetime + ".csv"
    _file = open(_filename, 'wb')
    _writer = csv.writer(_file, quoting=csv.QUOTE_ALL)
    for item in _stations:
        _writer.writerow(item)

# scrape the json data once every 2.5 minutes (150sec) for 3 days, starting 5sec from now
run_periodically(time()+5, time()+(3*24*60*60), 150, write_stations)