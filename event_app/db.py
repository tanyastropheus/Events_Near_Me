#!/usr/bin/python3
'''
index = 'events'
doc_type = 'info'
'''

import requests, urllib
from elasticsearch import Elasticsearch
from pprint import pprint  # REVISIT: for debugging purpose only.

class DB():
    '''DB class that handles setup and other db-related operations'''
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
                    "char_filter": ['html_strip'], # strips '\n' in description field
                    "filter": [
#                        "synonym",
                        "asciifolding",  # for accents
                        "english_possessive_stemmer",
                        "lowercase",
                        "english_stop",
                        "english_stemmer"
                    ]
                }
            }
        }
    }

    def __init__(self, index, doc_type):
        self.index = index
        self.doc_type = doc_type
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def create_index(self):
        '''create empty index with customized setting & mapping'''

        # define mapping to allow geo point data type
        mapping = {
            "properties" : {
                "address" : {"type" : "keyword"},
                "location": {"type": "geo_point"},
                "cost" : {"type" : "long"},
                "date" : {"type" : "keyword"}, # REVISIT with date datatype
                "link" : {"type" : "keyword"},
                "name" : {
                    "type": "text",
                    "fields": {
                        "keyword_string": {
                            "type": "text",
                            "analyzer": "english_synonym"
                        },
                        "completion": {
                            "type": "completion"
                        }
                    }
                },
                "tags" : {"type" : "text", "analyzer": "english_synonym"},
                "time" : {"type" : "keyword"}, # REVISIT
                "image_url": {"type": "keyword"},
                "description": {"type" : "text", "analyzer": "english_synonym"},
                "venue": {"type": "keyword"}
            }
        }

        setting = {
            "settings": self.english_synonym,
            "mappings": {self.doc_type: mapping}
        }
        self.es.indices.create(index=self.index, body=setting)

    """
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
    """
    def get_tokens(self, anal_type, anal_name, text, index=None):
        ''''
        Return a list of tokens based on the standard tokenizer.

        Args:
            text (str): text to be tokenized
        '''

        body = {
            anal_type: anal_name,
            "text": ""
        }

        body['text'] = text
        results = self.es.indices.analyze(index=index, body=body)
        tokens = []
        for i in range(len(results['tokens'])):
            tokens.append(results['tokens'][i]['token'])
        return tokens

    def delete_index(self):
        '''delete existing index'''
        if self.es.indices.exists(index=self.index):
            self.es.indices.delete(index=self.index)

    def store_doc(self, doc_id, data):
        '''store event data in designated index and doc_type'''
        self.es.index(index=self.index, doc_type=self.doc_type, id=doc_id, body=data)

    def search(self, query):
        '''search index for docs that match query string'''
        # will pass the query to the function instead of setting inside the function
        '''
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

        if q_multi == True:
            body = multi_query
        else:
            body = single_query
        '''
        results = self.es.search(index=self.index, doc_type=self.doc_type, body=query)
        print("from db query")
        pprint(results)
        return results

    def auto_complete(self, user_input=""):
        '''queries database in real time as user inputs data'''
        auto_query = {
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

    def get_num_docs(self):
        '''return the number of docs saved in an index'''
        if self.es.indices.exists(index=self.index):
            num_docs = self.es.count(index=self.index, doc_type=self.doc_type)['count']
            print("number of documents: ", num_docs)

        return num_docs


    def addr_to_geo(self, doc_id):
        '''
        Look up latitude & longitude based on address for the doc id specified.

        Returns:
            A dict of location in lat & lon.
            e.g. {'doc': {'location': {'lat': lat, 'lon': lng}}}
        '''
        api_key = 'AIzaSyDMZ83GsgwA4MGa52utHcrdwufwdE6aCDc'

        addr = self.es.get(index=self.index, doc_type=self.doc_type, id=doc_id)['_source']['address']
#        print(addr)
        addr_lookup = {'address': addr, 'key': api_key}
        addr_url = urllib.parse.urlencode(addr_lookup)
        geo = requests.get('https://maps.googleapis.com/maps/api/geocode/json?{}'.format(addr_url))
        geo.connection.close()
        if geo.status_code == 200:
            lat = geo.json()['results'][0]['geometry']['location']['lat']
            lng = geo.json()['results'][0]['geometry']['location']['lng']
            geo_location = {'doc': {'location': {'lat': lat, 'lon': lng}}}
#            print(geo_location)
            return geo_location
        else:
            print("geo request failed")


    def save_geo(self, doc_id, geo_location):
        '''save the geo-coordinates to ES for the doc id specified'''
        self.es.update(index=self.index, doc_type=self.doc_type, id=doc_id, body=geo_location)
