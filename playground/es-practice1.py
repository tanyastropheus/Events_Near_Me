#!/usr/bin/python3
'''Playing with python elasticsearch low level client'''
import requests, json, urllib.parse
import sys
from pprint import pprint
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, DocType
'''
# check ES is up and running
res = requests.get('http://localhost:9200')
print(res.content)
'''

# connect to ES server
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

'''
if es.indices.exists(index='event_test'):
    es.indices.delete(index='event_test')
    sys.exit()
'''

# define mapping to allow geo point data type
mapping = {
    "properties" : {
        "address" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
            }
        },
        "location": {
            "type": "geo_point"
        },
        "cost" : {
            "type" : "long"
        },
        "date" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
            }
        },
        "link" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
            }
        },
        "name" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
            }
        },
        "tags" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
            }
        },
        "time" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
            }
        }
    }
}

'''
# create index
es.indices.create('event_test')

# defined mapping for the index
es.indices.put_mapping(index='event_test', doc_type='practice', body=mapping)
'''

event1 = {
    'address': '533 Sutter Street, San Francisco, CA',
    'cost': 0,
    'date': 'Fri Feb 9',
    'link': 'https://www.sfstation.com//dj-karma-at-flightfridays-e2339977',
    'name': 'DJ Karma at #FlightFridays',
    'tags': ['Clubs', 'Music'],
    'location': {
        'lat': 0.0,
        'lon': 0.0
    },
    'time': '9p-2a'}

event2 = {
    'address': '124 Ellis Street, San Francisco, CA',
    'cost': 30,
    'date': 'Fri Feb 9',
    'link': 'https://www.sfstation.com//flight-fridays-guest-list-2-9-2018-e2338597',
    'name': 'Flight Fridays Guest List - 2.9.2018',
    'tags': ['Arts', 'Comedy', 'Theater', 'Performance Arts', 'Spoken Word'],
    'location': {
        'lat': 0.0,
        'lon': 0.0
    },
    'time': '09:00 PM'}

event3 = {
    'address': '540 Howard Street, San Francisco, CA',
    'cost': 15,
    'date': 'Fri Feb 9',
    'link': 'https://www.sfstation.com//don-diablo-e2338813',
    'name': 'Don Diablo',
    'tags': ['Clubs',
             'Music',
             'Dance Club',
             "DJ's",
             'Electronic Music',
             'Hip Hop',
             'House Music'],
    'location': {
        'lat': 0.0,
        'lon': 0.0
    },
    'time': '10pm-2am'}

event4 = {
    'address': '20 Woodside Avenue, San Francisco, CA',
    'cost': 55,
    'date': 'Fri Feb 9',
    'name': 'THOMAS SCHULTZ, pianist, plays two virtuoso pieces by Arnold Schoenberg',
    'tags': ['Family'],
    'location': {
        'lat': 0.0,
        'lon': 0.0
    },
    'time': '4pm'}


event5 = {
    'address': '210 Post St, San Francisco, CA',
    'cost': 0,
    'date': 'Fri Feb 9',
    'name': 'Udo Nöger: The Inside of Light',
    'tags': ['Arts', 'Art Opening', 'Art Exhibit'],
    'location': {
        'lat': 0.0,
        'lon': 0.0
    },
    'time': '01:00pm'}

'''
# store event data using elasticsearch
es.index(index='event_test', doc_type='practice', id=0, body=event1)
es.index(index='event_test', doc_type='practice', id=1, body=event2)
es.index(index='event_test', doc_type='practice', id=2, body=event3)
es.index(index='event_test', doc_type='practice', id=3, body=event4)
es.index(index='event_test', doc_type='practice', id=4, body=event5)
'''


# query data with specific tags
# terms search through inverted index, which converts tokens into lowercase
print("All events with the tag 'Family' and/or 'Arts':")
pprint(es.search(index='event_test', doc_type='practice',
                 body={"query": {
                     'constant_score': {
                         'filter': {
                             'terms': {  # search multiple terms (or)
                                 'tags': ['family', 'arts']
                             }
                         }
                     }
                 }
                   }))

# query data with cost range
print("All events with price range between 0 and 30:")
pprint(es.search(index='event_test', doc_type='practice',
                 body={"query": {
                     'constant_score': {
                         'filter': {
                             'range': {
                                 'cost': {
                                     'gte': 0,
                                     'lt': 30
                                 }
                             }
                         }
                     }
                 }
                   }))

'''
# Getting specific field attribute values
pprint(es.get(index='event_test', doc_type='practice', id=1))
pprint(es.count(index='event_test', doc_type='practice')['count'])
pprint(es.get(index='event_test', doc_type='practice', id=1)['_source']['address'])
'''

'''
# Look up longitude & latitude based on address && save it to ES
api_key = 'AIzaSyAkdExJFmcG7SqmXTp481KAieX82H4NjGY'
num_docs = es.count(index='event_test', doc_type='practice')['count']
print(num_docs)

i = 0
while i < num_docs:
    print('insdie')
    addr = es.get(index='event_test', doc_type='practice', id=i)['_source']['address']
    print(addr)
    addr_lookup = {'address': addr, 'key': api_key}
    addr_url = urllib.parse.urlencode(addr_lookup)
    geo = requests.get('https://maps.googleapis.com/maps/api/geocode/json?' + addr_url)

    if geo.status_code == 200:
        lat = geo.json()['results'][0]['geometry']['location']['lat']
        lng = geo.json()['results'][0]['geometry']['location']['lng']
        location = {'doc': {'location': {'lat': lat, 'lon': lng}}}
        print(location)
        es.update(index='event_test', doc_type='practice', id=i, body=location)
    else:
        print("geo request failed")
        sys.exit()
    i += 1
'''
