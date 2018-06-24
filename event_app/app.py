#!/usr/bin/python3

import requests, json, copy, sys
print(sys.path)
from event_app.db import DB
from pprint import pprint
from elasticsearch import Elasticsearch
from flask import abort, Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = DB("events_today", "info")
#db.delete_index()
#db = DB('test_fulltext_search', 'test_fulltextdoc')
#db = DB('event_test', 'event_info')

"""
filename = '/tests/test_data.txt'
#db = DB('test_compound_search', 'test_compound_doc')
db.delete_index()


# check ES is up and running
res = requests.get('http://localhost:9200')
print(res.status_code)

def load_data_from_file(filename):
    '''read data from test data file.

    Returns:
        List of event dicts.
    '''
    text = ""
    with open(filename) as f:
        for line in f:
            li = line.strip()
            if not li.startswith('#'):
                text += line
    events = json.loads(text, strict=False)
    return events


def store_docs(events):
    '''store event data in elasticsearch.

    Args:
    events(list): a list of event data in dictionary form
                  e.g. [event1, event2...] where each event is a dict

    Note: document id starts with 0
    '''
    i = 0
    while i < len(events):
        event = "event" + str(i + 1)
        db.store_doc(i, events[i][event])
        i += 1

def DBsetUP():
    '''set up test database and load test data'''
    db.create_index()

    # save test data from file to the database
    events = load_data_from_file(filename)
    store_docs(events)

    # allow time for Elasticsearch server to store all data
    time.sleep(3)

    # look up & save geolocation to db based on address
    num_docs = db.get_num_docs()
    for i in range(num_docs):
        geo = db.addr_to_geo(i)
        db.save_geo(i, geo)
        i += 1

    # allow time for Elasticsearch server to store all data
    time.sleep(3)

DBsetUP()

"""
@app.route('/index')
def main():
    return render_template('index.html')

@app.route('/api/event_auto_complete', methods=['POST', 'GET'])
def auto_complete():
    '''queries database in real time as user inputs data'''
    params = request.get_json()
    user_input = params['keywords']

    query = {
        'suggest': {
            'event-suggest': {
                "prefix": user_input,
                "completion": {
                    "field": "name"
                }
            }
        }
    }
    results = self.es.search(index=self.index, doc_type=self.doc_type, body=query)


@app.route('/api/event_search', methods=['POST', 'GET'])
def event_search():
    """return events searched by the user"""
    params = request.get_json()

    if params is None:
        print("params is none")
        abort(404)

    # check cost input
    try:
        float(params['cost'])
        if float(params['cost']) < 0:
            print("cost < 0")
            abort(404)
    except ValueError:
        if params['cost'] == "100+":
            params['cost'] = 10000
        else:
            print("cost abort")
            abort(404)

    # check radius input
    try:
        float(params['radius'][:-2])
        if float(params['radius'][:-2]) <= 0:
            print("radius negative")
            abort(404)
    except ValueError:
        print("radius not a number")
        abort(404)

    cost_geo_query = {
        'bool': {
            'must': [{
                'geo_distance': {
                    'distance': params['radius'],
                    'location': {
                        'lat': params['user_location']['lat'],
                        'lon': params['user_location']['lng']
                    }
                }
            },
                {'range': {
                    'cost': {
                        'gte': -1, 'lte': params['cost']
                    }
                }
             }]
        }
    }

    all_events_query = {
        'from': 0, 'size': 10000,
        'query': {
            'constant_score': {
                'filter': cost_geo_query
            }
        }
    }

    event_query = {
        'from': 0, 'size': 10000,
        'query': {
            'bool': {
                'must': {
                    'multi_match': {'query': "",
                                    'analyzer': 'english_synonym',
                                    'fields': ['name', 'tags'],
                                    'type': 'best_fields',
                                    'minimum_should_match': '85%',
                                    'fuzziness': 'AUTO'
                                }
                },
                'filter': cost_geo_query
            }
        }
    }

    if 'Any' in params['tags']:
        body = all_events_query
    elif params['tags']:
        tag_string = ""
        for tag in params['tags']:
            tag_string += tag + ' '
        event_query['query']['bool']['must']['multi_match']['query'] = tag_string.strip()
        body = event_query
    elif params['keywords']:
        event_query['query']['bool']['must']['multi_match']['query'] = params['keywords']
        body = event_query
    else:
        data = {}


    try:
        print("data sent to ES:")
        pprint(body)
        data = db.search(body)
    except UnboundLocalError:
        print("exception")
        pass

    print("data from endpoint:")
    pprint(data)
    return json.dumps(data)

@app.route('/api/all_events')
def all_events():
    '''return all event data from DB'''
    # get total number of events
    num_events = es.count(index=index_name, doc_type=doc_type_name)['count']

    events = {}  # a dict of event dicts
    i = 1
    while i <= num_events:
        event = {}  # {id: {'name': 'e_name', 'address': 'e_addr',...}}
        event[i] = es.get(index=index_name, doc_type=doc_type_name, id=str(i))['_source']
        events.update(event)
        i += 1

    pprint(events)
    print("num_events: ", num_events)
    return json.dumps(events)


@app.route('/map/all')
def all_events_map():
    '''drop pins based on lat&lon from ES using test'''
    '''(index = event_test, doctype = practice)'''
    return render_template('test_all_from_DB.html')

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
