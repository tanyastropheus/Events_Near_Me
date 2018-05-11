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

# combined queries
geo_only_query = {
    'geo_distance': {
        'distance': "100mi",
        'location': {
            'lat': 37.773972,
            'lon': -122.431297
        }
    }
}


# This works!
geo_full_query = {
    'query': geo_only_query
}

cost_only_query = {
    'range': {
        'cost': {
            'gte': 0, 'lte': 1000
            }
    }
}

# This works
cost_full_query = {
    'query': {
        'constant_score': {
            'filter': cost_only_query
        }
    }
}

event_tag_query = {
    'terms': {
        'tags': ["art", "club"]
    }
}

all_events_query = {
    'query': {
        'constant_score': {
            'filter': {
                'bool': {
                    'must': [
                        cost_only_query,
                        geo_only_query
                    ]
                }
            }
        }
    }
}

# This works
no_keywords_query = {   # need to implement date & time range
    'query': {
        'bool': {
            'must': {
                'multi_match': {
                    'query': "art/club",
                    'fields': "tags",
                    'fuzziness': 'AUTO'
                }
            },
            'should': {
                'multi_match': {
                    'query': "art/club",
                    'fields': 'name',
                    'fuzziness': 'AUTO'
                }
            },
            'filter': {
                'bool': {
                    'must': [
                        cost_only_query,
                        geo_only_query
                    ]
                }
            }
        }
    }
}

# This works
keywords_query = {   # need to implement date & time range
    'query': {
        'multi_match': {  # REVISIT: add boost to specific fields
            'query': "Friday light",
            'type': 'best_fields',  # the default
            'fields': ['name', 'tags'],
            'fuzziness': 'AUTO'  # in case of user typo
            # REVISIT: Set Analyzer for intelligently finding synonyms
        }
    }
}

# this works!
keywords_query_plus_filter = {   # need to implement date & time range
    'query': {
        'bool': {
            'must': {
                'multi_match': {  # REVISIT: add boost to specific fields
                    'query': "Friday music",
                    'type': 'best_fields',  # the default
                    'fields': ['name', 'tags'],
                    'fuzziness': 'AUTO'  # in case of user typo
                    # REVISIT: set minimum_should_match %
                    # to display more relevant results
                    # REVISIT: Set Analyzer for intelligently finding synonyms
                }
            },
            'filter': {
                'bool': {
                    'must': [
                        cost_only_query,
                        geo_only_query
                    ]
                }
            }
        }
    }
}

print("All events containing the keywords:")
del no_keywords_query['query']['bool']['must']
del no_keywords_query['query']['bool']['should']

pprint(no_keywords_query)
pprint(es.search(index='event_test', doc_type='practice', body=keywords_query))

'''
# Getting specific field attribute values
pprint(es.get(index='event_test', doc_type='practice', id=1))
pprint(es.count(index='event_test', doc_type='practice')['count'])
pprint(es.get(index='event_test', doc_type='practice', id=1)['_source']['address'])
'''
