from flask import Flask, render_template, url_for, request, jsonify, json
from getstations import get_stations, num_free_bikes, get_recent_statuses

app = Flask(__name__)

@app.route('/get_recent_history', methods=['GET', 'POST'])
def return_historical_markers():
    # grab the station history dict
    _stationhistorydict = get_recent_statuses()
    reformatted_history_list = []
    # go through all keys (timestamps) in the dict
    for _timestamp in _stationhistorydict:
        reformatted_stations = []
        # go through all the stations at that timestamp
        for st in _stationhistorydict[_timestamp]:
            # reformat into a dict
            reformatted_stations.append({
                'name': st[0],
                'stationid' : st[1],
                'totaldocks' : st[3], 
                'availabledocks' : st[2], 
                'latLng' : [float(st[4]), float(st[5])],
                'numbikes' : num_free_bikes(int(st[2]), int(st[3])),
                'timestamp' : _timestamp
            })
        reformatted_history_list.append(reformatted_stations)
    # return a jsonified list of lists of dictionaries
    return jsonify(historylist=reformatted_history_list)
    

@app.route('/get_stations', methods=['GET', 'POST'])
def return_markers():
    # grab the current station statuses from citibike
    _stations = get_stations()
    # create a new, re-formatted stations list
    reformatted_stations = []
    for st in _stations:
        reformatted_stations.append({
            'name': st[0],
            'stationid' : st[1],
            'totaldocks' : st[3], 
            'availabledocks' : st[2], 
            'latLng' : [st[4], st[5]],
            'numbikes' : num_free_bikes(st[2], st[3])
        })
    return jsonify(stations=reformatted_stations)

@app.route('/')
def index():
    # just render the html page
	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)