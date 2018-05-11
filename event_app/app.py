#!/usr/bin/python3

import requests, json
import copy
from pprint import pprint
from elasticsearch import Elasticsearch
from flask import abort, Flask, render_template, jsonify, request
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
def event_search():
    """return events searched by the user"""
    if request.get_json() is None:
        abort(404)

    index_name = 'event_test'
    doc_type_name = 'practice'
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

    cost_geo_query =  {
        'bool': {
            'must': [
                cost_only_query,
                geo_only_query
            ]
        }
    }

    multi_match_query = {
        'multi_match': {  # REVISIT: add boost to specific fields
            'query': '',  # query strings to be matched from docs
            'type': 'best_fields',  # the default; Finds documents which match any field, but uses the _score from the best field
            'fields': '',
            'fuzziness': 'AUTO'  # in case of user typo
            # REVISIT: Set Analyzer for intelligently finding synonyms
        }
    }

    event_query = {   # need to implement date & time range
        'query': {
            'bool': {
                'must': multi_match_query,
                'should': multi_match_query,
                'filter': cost_geo_query
            }
        }
    }

    all_events_query = {
        'query': {
            'constant_score': {
                'filter': cost_geo_query
            }
        }
    }

    if not params['keywords']:  # event tags only
        if 'Any' in params['tags']:
            print("inside")
            # query all events that meet other search criteria
            data = es.search(index=index_name, doc_type=doc_type_name,
                             body=all_events_query)
        else:
            # query events with matching tags
            # must search matching strings from event tags (AND)
            must_query = copy.deepcopy(multi_match_query)
            tag_string = ""
            for tag in params['tags']:
                tag_string += tag + ' '
            must_query['multi_match']['query'] = tag_string.strip()
            must_query['multi_match']['fields'] = 'tags'

            # should also search match strings from event name (OR)
            should_query = copy.deepcopy(multi_match_query)
            should_query['multi_match']['query'] = tag_string.strip()
            should_query['multi_match']['fields'] = 'name'

            event_query['query']['bool']['must'] = must_query
            event_query['query']['bool']['should'] = should_query
            data = es.search(index=index_name, doc_type=doc_type_name,
                             body=event_query)
    else: # keywords only
        # full text search
        keywords_query = copy.deepcopy(multi_match_query)
        keywords_query['multi_match']['query'] = params['keywords']
        keywords_query['multi_match']['fields'] = ['name', 'tags']
        event_query['query']['bool']['must'] = keywords_query
        del event_query['query']['bool']['should']
        data = es.search(index=index_name, doc_type=doc_type_name,
                         body=event_query)

    pprint(data)
    return json.dumps(data)

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
