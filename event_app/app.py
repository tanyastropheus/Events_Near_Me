#!/usr/bin/python3

import requests, json, copy, sys
print(sys.path)
from event_app import db
from pprint import pprint
from elasticsearch import Elasticsearch
from flask import abort, Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/index')
def main():
    return render_template('index.html')

@app.route('/api/event_suggestions', methods=['POST', 'GET'])
def get_event_suggestions():
    '''queries database in real time to return a list of suggested events
    as user inputs data'''
    user_input = request.get_json()
    query = {
        'suggest': {
            'event_suggest': {
                "prefix": user_input,
                "completion": {
                    "size": 20,
                    "field": "suggest.completion",
                }
            }
        }
    }
    results = db.search(query)
    return json.dumps(results)


@app.route('/api/event_title', methods=['POST', 'GET'])
def get_event():
    '''return the event user selected from the autocomplete suggester'''
    event_title = request.get_json()
    query = {
        'query': {
            'term': {
                'name.exact_search': event_title
            }
        }
    }
    result = db.search(query)
    return json.dumps(result)


@app.route('/api/event_search', methods=['POST', 'GET'])
def event_search():
    """
    Return events searched by the user through selected event tags and keywords
    """
    params = request.get_json()

    if params is None:
        print("params is none")
        abort(404)

    # check cost input
    try:
        float(params['cost'])
        if float(params['cost']) < 0:
            abort(404)
    except ValueError:
        if params['cost'] == "100+":
            params['cost'] = 10000
        else:
            abort(404)

    # check radius input
    try:
        float(params['radius'][:-2])
        if float(params['radius'][:-2]) <= 0:
            abort(404)
    except ValueError:
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
                                    'analyzer': 'event_english',
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
