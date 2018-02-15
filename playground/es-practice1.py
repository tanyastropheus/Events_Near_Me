#!/usr/bin/python3
'''Playing with python elasticsearch low level client'''
import requests, json
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

event1 = {
    'address': '533 Sutter Street, San Francisco, CA',
    'cost': 0,
    'date': 'Fri Feb 9',
    'link': 'https://www.sfstation.com//dj-karma-at-flightfridays-e2339977',
    'name': 'DJ Karma at #FlightFridays',
    'tags': ['Clubs', 'Music'],
    'time': '9p-2a'}

event2 = {
    'address': '124 Ellis Street, San Francisco, CA',
    'cost': 30,
    'date': 'Fri Feb 9',
    'link': 'https://www.sfstation.com//flight-fridays-guest-list-2-9-2018-e2338597',
    'name': 'Flight Fridays Guest List - 2.9.2018',
    'tags': ['Arts', 'Comedy', 'Theater', 'Performance Arts', 'Spoken Word'],
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
    'time': '10pm-2am'}

event4 = {
    'address': '20 Woodside Avenue, San Francisco, CA',
    'cost': 55,
    'date': 'Fri Feb 9',
    'name': 'THOMAS SCHULTZ, pianist, plays two virtuoso pieces by Arnold Schoenberg',
    'tags': ['Family'],
    'time': '4pm'}


event5 = {
    'address': '210 Post St, San Francisco, CA',
    'cost': 0,
    'date': 'Fri Feb 9',
    'name': 'Udo Nöger: The Inside of Light',
    'tags': ['Arts', 'Art Opening', 'Art Exhibit'],
    'time': '01:00pm'}

'''
# store event data using elasticsearch
es.index(index='event_test', doc_type='practice', id=1, body=event1)
es.index(index='event_test', doc_type='practice', id=2, body=event2)
es.index(index='event_test', doc_type='practice', id=3, body=event3)
es.index(index='event_test', doc_type='practice', id=4, body=event4)
es.index(index='event_test', doc_type='practice', id=5, body=event5)
'''

# query data with specific tags
# terms search through inverted index, which converts tokens into lowercase
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
pprint(es.get(index='event_test', doc_type='practice', id=1))
pprint(es.get(index='event_test', doc_type='practice', id=2))
pprint(es.get(index='event_test', doc_type='practice', id=3))
'''
