#!/usr/bin/python3

import requests, urllib
from elasticsearch import Elasticsearch
from pprint import pprint  # REVISIT: for debugging purpose only.

class DB():
    '''DB class that handles setup and other db-related operations'''
    # customize analyzer for english stemming and possessives
    event_english = {
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
                }
            },
            "analyzer": {
                "event_english": {
                    "tokenizer":  "standard",
                    "char_filter": ['html_strip'], # strip '\n' in description
                    "filter": [
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
                        "keyword_search": {
                            "type": "text",
                            "analyzer": "event_english"
                        },
                        "exact_search" : {
                            "type": "keyword"
                        }
                    }
                },
                "suggest": {
                    "type": "text",
                    "fields": {
                        "completion": {
                            "type": "completion"
                        }
                    }
                },
                "tags" : {"type" : "text", "analyzer": "event_english"},
                "time" : {"type" : "keyword"}, # REVISIT
                "when" : {"type" : "keyword"},
                "image_url": {"type": "keyword"},
                "description": {"type" : "text", "analyzer": "event_english"},
                "venue": {"type": "keyword"}
            }
        }

        setting = {
            "settings": self.event_english,
            "mappings": {self.doc_type: mapping}
        }

        # create an index if not already exists
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(index=self.index, body=setting)

    def get_tokens(self, analyzer_type, analyzer_name, text, index=None):
        ''''
        Return a list of tokens based on the standard tokenizer.

        Args:
            text (str): text to be tokenized
        '''

        body = {
            analyzer_type: analyzer_name,
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
        self.es.index(index=self.index, doc_type=self.doc_type,
                      id=doc_id, body=data)

    def search(self, query):
        '''search index with the given query for matching docs'''
        results = self.es.search(index=self.index, doc_type=self.doc_type,
                                 body=query)
        print("from db query")
        pprint(results)
        return results

    def get_num_docs(self):
        '''return the number of docs in an index'''
        if self.es.indices.exists(index=self.index):
            num_docs = self.es.count(index=self.index, doc_type=self.doc_type)['count']
        print("number of documents:", num_docs)
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
        addr_lookup = {'address': addr, 'key': api_key}
        addr_url = urllib.parse.urlencode(addr_lookup)
        geo = requests.get('https://maps.googleapis.com/maps/api/geocode/json?{}'.format(addr_url))
        geo.connection.close()

        if geo.status_code == 200:
            lat = geo.json()['results'][0]['geometry']['location']['lat']
            lng = geo.json()['results'][0]['geometry']['location']['lng']
            geo_location = {'doc': {'location': {'lat': lat, 'lon': lng}}}
            return geo_location
        else:
            print("geo request failed")


    def save_geo(self, doc_id, geo_location):
        '''save the geo-coordinates to ES for the doc id specified'''
        self.es.update(index=self.index, doc_type=self.doc_type, id=doc_id, body=geo_location)
