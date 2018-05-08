#!/usr/bin/python3

import requests, json
from elasticsearch import Elasticsearch
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# check ES is up and running
res = requests.get('http://localhost:9200')
print(res.status_code)

# connect to ES server
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

@app.route('/index')
def main():
    return render_template('index.html')

@app.route('/api/event_search', methods=['POST', 'GET'])
def events_search():
    """return events searched by the user"""
    if request.get_json() is not None:
        params = request.get_json()
        geo_only_query = {
            'geo_distance': {
                'distance': params['radius'],
                'location': {
                    'lat': params['user_location']['lat'],
                    'lon': params['user_location']['lng']
                }
            }
        }

        cost_only_query = {
            'range': {
                'cost': {
                    'gte': 0, 'lte': params['cost']
                }
            }
        }

        event_tag_query = {
            'terms': {
                'tags': params['tags']
            }
        }

        no_keyword_query = {   # need to implement date & time range
            'query': {
                'constant_score': {
                    'filter': [
                        event_tag_query,
                        cost_query,
                        geo_query
                    ]
                }
            }
        }

        keywords_query = {   # need to implement date & time range
            'query': {
                'bool': {
                    'must': {
                        'match': {
                            'keywords': params['keywords']
                        }
                    },
                    'filter': {
                        cost_query,
                        geo_query
                    }
                }
            }
        }

        if not params['keywords']:  # event tags only
            if 'Any' in params['tags']:
                # query all events that meet other search criteria
                no_keyword_query['query']['constant_score']['filter'].remove(event_tag_query)
                print(no_keyword_query)
                data = es.search(index='event_test', doc_type='practice',
                                 body=no_keyword_query)
            else:
                # query events matching tags
                data = es.search(index='event_test', doc_type='practice',
                                 body=no_keyword_query)
        else: # keywords only
            # full text search
            data = es.search(index='event_test', doc_type='practice',
                             body=keyword_query)
        print(data)
        return data

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
