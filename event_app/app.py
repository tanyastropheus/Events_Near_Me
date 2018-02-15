#!/usr/bin/python3

import requests
from elasticsearch import Elasticsearch
from flask import Flask, render_template
app = Flask(__name__)

# check ES is up and running
res = requests.get('http://localhost:9200')
print(res.status_code)

# connect to ES server
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

@app.route('/')
def show_all():
    search_all = requests.get('http://localhost:9200/events/_search?pretty')
    return search_all.content

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/map')
def display_map():
    '''displays Google Map with Holberton School address hard-coded in'''
    return render_template('add_map.html')

@app.route('/map/geocoding')
def geocoding():
    '''drop pin based on address (using geocode to convert to long & lat)'''
    return render_template('geocoding.html')

@app.route('/map/info_window')
def info_window():
    '''current the same as geocoding; REVISIT'''
    return render_template('info_window.html')

@app.route('/map/geo_detect')
def geo_detect():
    '''detects user location based on user device'''
    return render_template('geo_detect.html')

@app.route('/map/geocoding_from_db')
def geocoding_from_db():
    '''drop pins based on address from test data (index = event_test)'''
    return render_template('geocoding_from_db.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
