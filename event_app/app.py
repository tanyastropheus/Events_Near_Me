#!/usr/bin/python3

import requests, json
from elasticsearch import Elasticsearch
from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# check ES is up and running
res = requests.get('http://localhost:9200')
print(res.status_code)

# connect to ES server
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

@app.route('/')
def show_all():
    '''displays event data stored in ES'''
    search_all = requests.get('http://localhost:9200/events/_search?pretty')
    return search_all.content

@app.route('/test')
def test():
    '''check that flask is up and serving the right webpages'''
    return render_template('test.html')

@app.route('/map')
def display_map():
    '''displays Google Map with Holberton school as the center view.  No pin'''
    return render_template('test_add_map.html')

@app.route('/map/geocoding')
def geocoding():
    '''test drop one pin based on hard-coded address'''
    '''using geocode to convert address to long & lat'''
    return render_template('test_geocoding.html')

@app.route('/api/all_events')
def all_events():
    '''return all event data from DB'''
    # index name to be queried
    idx_name = 'event_test'
    doc = 'practice'

    # get total number of events
    num_events = es.count(index=idx_name, doc_type=doc)['count']

    events = {}  # a dict of event dicts
    i = 0
    while i < num_events:
        event = {}  # {id: {'name': 'e_name', 'address': 'e_addr',...}}
        event[i] = es.get(index=idx_name, doc_type=doc, id=str(i))['_source']
        events.update(event)
        i += 1

    return json.dumps(events)

@app.route('/map/all')
def all_events_map():
    '''drop pins based on lat&lon from ES using test'''
    '''(index = event_test, doctype = practice)'''
    return render_template('test_all_from_DB.html')

# this is extra
@app.route('/map/geo_detect')
def geo_detect():
    '''detects user location based on user device'''
    return render_template('test_geo_detect.html')


"""no longer needed since geolocation is saved in ES
@app.route('/map/all')
def all_events():
    '''drop pins based on address from test data (index = event_test)'''
    # index name to be queried
    idx_name = 'event_test'
    doc = 'practice'

    # get total number of events
    num_events = es.count(index=idx_name, doc_type=doc)['count']

    events = {}  # a dict of event dicts
    i = 0
    while i < num_events:
        event = {}  # {id: {'name': 'e_name', 'address': 'e_addr',...}}
        event[i] = es.get(index=idx_name, doc_type=doc, id=str(i))['_source']
        events.update(event)
        i += 1

    # return json.dumps(events)
    return render_template('test_all.html')
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
