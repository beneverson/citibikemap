from flask import Flask, render_template, url_for, request, jsonify
from getstations import get_stations

app = Flask(__name__)

@app.route('/get_stations', methods=['GET', 'POST'])
def return_markers():
	markers = []
	stations = get_stations()
	for i in stations:
		markers.append({
			'type': 'Feature',
			'geometry': {
				'type': 'Point',
				'coordinates': [i[5], i[4]]
				},
			'properties': {
				'title': i[0],
				'description': (i[3] - i[2])/float(i[3]),
				'marker-size': 'medium',
				'marker-color': 'blue'
				}
		})
	return jsonify(markers=markers)

@app.route('/')
def index():
	return render_template('index.html')
		

if __name__ == '__main__':
    app.run(debug=True)