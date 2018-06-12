import sys, unittest, time, json
sys.path.append('..')
from elasticsearch import Elasticsearch
from event_app.db import DB
from pprint import pprint

db = DB('test_compound_search', 'test_compound_doc')
filename = 'test_data/test_data.txt'

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



class TestCompoundSearch(unittest.TestCase):
    '''
    Check that compound queries return corresponding documents stored in ElasticSearch.
    '''
    @classmethod
    def setUpClass(cls):
        '''set up the test database && load it with data'''
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


    @classmethod
    def tearDownClass(cls):
        '''delete test index'''
        db.delete_index()


    @staticmethod
    def get_doc_list(results):
        '''take search results and return a list of doc id's'''
        doc_list = []
        # return None if search has no result
        if results['_shards']['total'] != 0:
            for doc in results['hits']['hits']:
                doc_list.append(doc['_id'])
        return doc_list


    def test_geo_cost(self):
        '''test cost range query'''

        query = {
            'query': {
                'constant_score': {
                    'filter': {
                        'bool': {
                            'must': [{
                                'geo_distance': {
                                    'distance': "5mi",
                                    'location': {
                                        'lat': 37.781715,
                                        'lon': -122.408367
                                    }
                                }
                            },
                            {'range': {
                                'cost': {
                                    'gte': -1, 'lte': 50
                                }
                            }
                         }]
                        }
                    }
                }
            }
        }

        # CHECK: verify radius with event app
        results = db.search(query)
        self.assertCountEqual(TestCompoundSearch.get_doc_list(results),
                              ['2', '3', '4'])

        max_cost = query['query']['constant_score']['filter']['bool']['must'][1]['range']['cost']
        radius = query['query']['constant_score']['filter']['bool']['must'][0]['geo_distance']
        # test max cost
        max_cost['lte'] = 10000
        radius['distance'] = "50mi"
        results = db.search(query)
        self.assertCountEqual(TestCompoundSearch.get_doc_list(results),
                         ['0', '1', '2', '3', '4'])

        # test min cost
        max_cost['lte'] = 0
        results = db.search(query)
        self.assertCountEqual(TestCompoundSearch.get_doc_list(results),
                              ['0', '4'])


    def test_event_search(self):
        '''
        test that a fulltext search is performed on the event query string
        for the multiple fields specified with the given filter
        '''
        query = {
            'query': {
                'bool': {
                    'must': {
                        'multi_match': {'query': 'music dance',
                                        'analyzer': 'english_synonym',
                                        'fields': ['name', 'description', 'tags'],
                                        'fuzziness': 'AUTO'
                                    }
                        },
                    'filter': {
                        'bool': {
                            'must': [{
                                'geo_distance': {
                                    'distance': "50mi",
                                    'location': {
                                        'lat': 37.781715,
                                        'lon': -122.408367
                                    }
                                }
                            },
                                {'range': {
                                    'cost': {
                                        'gte': -1, 'lte': 40
                                    }
                                }
                             }]
                        }
                    }
                }
            }
        }
        results = db.search(query)
        self.assertCountEqual(TestCompoundSearch.get_doc_list(results), ['0', '1', '2'])

        # checking the filter on query string
        query_string = query['query']['bool']['must']['multi_match']
        query_string['query'] = "musical dancing"
        results = db.search(query)
        self.assertCountEqual(TestCompoundSearch.get_doc_list(results), ['0', '1', '2'])

        query_string['query'] = 'Food/Drinks + the color purple'
        results = db.search(query)
        pprint(results)
        self.assertCountEqual(TestCompoundSearch.get_doc_list(results), ['2', '3', '4'])


if __name__ == "__main__":
    unittest.main()
