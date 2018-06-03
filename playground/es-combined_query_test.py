#!/usr/bin/python3
'''Playing with python elasticsearch low level client'''
import requests, json, urllib.parse, sys, time
from pprint import pprint
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, DocType

# connect to ES server
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

index = 'event_test'
doc_type = 'event_info'

def check_setup():
    '''check ES is up and running'''
    res = requests.get('http://localhost:9200')
    print(res.content)

def delete_index(index):
    '''delete index if it exists'''
    if es.indices.exists(index=index):
        es.indices.delete(index=index)

def create_index(index):
    '''create empty index with customized setting & mapping'''
 # customize analyzer for english stemming, possessives, and synonyms
    english_synonym = {
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords":  "_english_"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                },
                "synonym": {  # set synonym filter with synonyms from WordNet
                    "type": "synonym",
                    "format": "wordnet",
                    "synonyms_path": "analysis/wn_s.pl"
                }
            },
            "analyzer": {
                "english_synonym": {
                    "tokenizer":  "standard",
                    "filter": [
                        "synonym",  # does not work as well
                        "asciifolding",  # for accents
                        "english_possessive_stemmer",
                        "lowercase",
                        "english_stop",
                        "english_stemmer"  # play with different aggressive levels
                    ]
                }
            }
        }
    }

    # defineA mapping to allow geo point data type
    mapping = {
        "properties" : {
            "address" : {"type" : "keyword"},
            "location": {"type": "geo_point"},
            "cost" : {"type" : "long"},
            "date" : {"type" : "keyword"}, # REVISIT with date datatype
            "link" : {"type" : "keyword"},
            "name" : {"type" : "text", "analyzer": "english_synonym"},
            "tags" : {"type" : "text", "analyzer": "english_synonym"},
            "time" : {"type" : "keyword"}, # REVISIT
            "image_url": {"type": "keyword"},
            "description": {"type" : "text", "analyzer": "english_synonym"},
            "venue": {"type": "keyword"}
        }
    }

    setting = {
        "settings": english_synonym,
        "mappings": {"event_info": mapping}
    }

    # create index if it doesn't already exist
    if not es.indices.exists(index=index):
        es.indices.create(index=index, body=setting)

def store_docs(index, doc_type, events):
    '''store event data in elasticsearch.

    Args:
        events(list): a list of event data in dictionary form
            e.g. [event1, event2...] where each event is a dict

    Note: document id starts with 0
    '''
    i = 0
    while i < len(events):
        event = "event" + str(i + 1)
        es.index(index=index, doc_type=doc_type, id=i, body=events[i][event])
        i += 1


def get_num_docs(index, doc_type):
    '''return the number of docs saved in an index'''
    if es.indices.exists(index=index):
        num_docs = es.count(index=index, doc_type=doc_type)['count']
        print("number of documents: ", num_docs)

    return num_docs


def addr_to_geo(index, doc_type, doc_id):
    '''
    Look up latitude & longitude based on address for the doc id specified.

    Returns:
        A dict of location in lat & lon.
        e.g. {'doc': {'location': {'lat': lat, 'lon': lng}}}
    '''
    api_key = 'AIzaSyAgPeDFl_wsFFzBfmtG0HY77Z_UXYYsiOE'

    addr = es.get(index=index, doc_type=doc_type, id=i)['_source']['address']
    print(addr)
    addr_lookup = {'address': addr, 'key': api_key}
    addr_url = urllib.parse.urlencode(addr_lookup)
    geo = requests.get('https://maps.googleapis.com/maps/api/geocode/json?{}'.format(addr_url))

    if geo.status_code == 200:
        lat = geo.json()['results'][0]['geometry']['location']['lat']
        lng = geo.json()['results'][0]['geometry']['location']['lng']
        geo_location = {'doc': {'location': {'lat': lat, 'lon': lng}}}
        print(geo_location)
        return geo_location
    else:
        print("geo request failed")
        sys.exit()


def save_geo(index, doc_type, doc_id, geo_location):
    '''save the geo-coordinates to ES for the doc id specified'''
    es.update(index=index, doc_type=doc_type, id=doc_id, body=geo_location)


def read_data_from_file(filename):
    '''read event data from test file.

    Returns:
        List of event dicts.
    '''
    # remove comments from file - is there a faster way to do this?
    text = ""
    with open(filename) as f:
        for line in f:
            li = line.strip()
            if not li.startswith('#'):
                text += line
    events = json.loads(text)
    return events


def view_tokens(events, field, proc_type, proc_name):
    '''
    Print a list of tokens based on the analyzer/tokenizer chosen.

    Args:
        events (list of dicts): events
        field (str): field of the event to be tokenized
        proc_type (str): "analyzer" or "tokenizer"
        proc_name (str): name of the proc_type
    '''

    body = {
        proc_type: proc_name,
        "text": ""
    }

    print('{}: {}'.format(proc_type, proc_name))
    for i in range(len(events)):
        text = events[i]['event' + str(i + 1)][field]
        body['text'] = text
        print(text)
        results = es.indices.analyze(index=index, body=body)
        print("tokens: ")

        tokens = []
        for j in range(len(results['tokens'])):
            tokens.append(results['tokens'][j]['token'])

        pprint(tokens)


def search(index, doc_type, q_string):
    '''search index for matching query docs'''
    multi_query = {
        'query': {
            'multi_match': {
                'query': q_string,
                'type': 'best_fields',
                'analyzer': 'english_synonym',
                'fields': ['name', 'description', 'tags'],
                'fuzziness': 'AUTO'
            }
        }
    }

    single_query = {
        'query': {
            'match': {
                'description': {
                    'query': q_string,
                    'analyzer': 'english_synonym'
                    }
            }
        }
    }

    print("query:", q_string)
    results = es.search(index=index, doc_type=doc_type, body=multi_query)
    pprint(results)

if __name__ == '__main__':
    # delete existing index and create a new one to laod new data

    delete_index(index)
    create_index(index)


    filename = 'stemmer_test_data.py'
    events = read_data_from_file(filename)
#    view_tokens(events, "description", "analyzer", "english_synonym")

    # store new data
    store_docs(index, doc_type, events)

    # allow es server time to store all data
    time.sleep(3)

    # verify the index is not empty
    get_num_docs(index, doc_type)

    # search docs with test queries
    search(index, doc_type, "hate")
    '''
    # save data location in geo-coordinates
    num_docs = get_num_docs(index=index, doc_type=doc_type)
    i = 0
    while i < num_docs:
        geo = addr_to_geo(index=index, doc_type, i)
        save_geo(index=index, doc_type=doc_type, i, geo)
        i += 1
    '''

'''
# update mapping after index creation
es.indices.put_mapping(index='event_test', doc_type='event_info', body=setting['mappings']['event_info'])
'''
'''
# query data with specific tags
# terms search through inverted index, which converts tokens into lowercase
print("All events with the tag 'Family' and/or 'Arts':")
pprint(es.search(index='event_test', doc_type='event_info',
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
pprint(es.search(index='event_test', doc_type='event_info',
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
'''
# combined queries
geo_only_query = {
    'geo_distance': {
        'distance': "6mi",
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
'''
'''
print("All events containing the keywords:")
del no_keywords_query['query']['bool']['must']
del no_keywords_query['query']['bool']['should']

pprint(no_keywords_query)

pprint(es.search(index='event_test', doc_type='event_info', body=keywords_query))
'''
'''
# Getting specific field attribute values
pprint(es.get(index='event_test', doc_type='event_info', id=1))
pprint(es.count(index='event_test', doc_type='event_info')['count'])
pprint(es.get(index='event_test', doc_type='event_info', id=1)['_source']['address'])
'''
