import sys, unittest, time, json
sys.path.append('..')
from elasticsearch import Elasticsearch
from event_app.db import DB

db = DB('test_fulltext_search', 'test_doc')
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
    events = json.loads(text)
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



class TestFullTextSearch(unittest.TestCase):
    '''
    Check that full-text queries return corresponding documents stored in ElasticSearch.
    '''
    # create empty query template to the database
    # run query first without setting query analyzer
    # then do it again by setting query analyzer to compare results
    query = {
        'query': {
            'multi_match': {
                'query': "",
                'type': 'best_fields',
                'analyzer': 'english_synonym',
                'fields': ['name', 'description', 'tags'],
                'fuzziness': 'AUTO'
            }
        }
    }

    @classmethod
    def setUpClass(cls):
        '''set up the test database with test data
        && create query template'''
        db.delete_index()
        db.create_index()

        # save test data from file to the database
        events = load_data_from_file(filename)
        store_docs(events)

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

    def test_fuzziness(self):
        '''one word query string with typo;
        query one field with a unique word'''

        '''do another one with more typo where ES won't be able to search
        given the AUTO fuzziness setting'''

        self.query['query']['multi_match']['query'] = "beutiful"
        results = db.search(self.query)
        self.assertEqual(TestFullTextSearch.get_doc_list(results), ['4', '1'])

        # This query returns no result; ES only supports fuzziness of 2
        self.query['query']['multi_match']['query'] = "biutiful"
        results = db.search(self.query)
        # TestFullTextSearch.get_doc_list ?
        self.assertNotEqual(self.get_doc_list(results), ['2', '4'])


    def test_no_result(self):
        '''send random query "498halbqwn" that has no search result'''
        self.query['query']['multi_match']['query'] = "498halbqwn"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), [])


    def test_empty_query(self):
        '''search with empty query'''
        self.query['query']['multi_match']['query'] = ""
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), [])


    def test_possessive(self):
        '''given "Amys" will return results like "Amy's"
        given DJ will return DJ's'''

        # check "DJ" will return results containing "DJ's"
        self.query['query']['multi_match']['query'] = "DJ"
        results = db.search(self.query)

        self.assertEqual(self.get_doc_list(results), ['3'])

        # check "Amys" will return results containing "Amy's"
        self.query['query']['multi_match']['query'] = "Amys"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), ['4'])

        # check "simpson's" will return results containing "Simpson"
        self.query['query']['multi_match']['query'] = "simpson's"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), ['3'])


    def test_search_tag(self):
        '''send in tag string and search tag'''
        # Combine event tags to generate query string
        # check "Food/Drinks" also return results containing  "Food", "Drink"
        self.query['query']['multi_match']['query'] = "Food/Drinks Performance Arts"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), ['4', '2', '3'])

        # mixing keyword with tag string
        self.query['query']['multi_match']['query'] = "Dance Club salsa"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), ['2', '1', '3'])


    def test_ascii(self):
        '''
        Check that asciifolding filter applies to both the query string and
        the indexed docs.
        '''
        # asciifolding filter does not translate
        # "christmas" !=> "noël"
        self.query['query']['multi_match']['query'] = "christmas"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), [])

        # accented query can return non-accented results, and vice versa
        # "Pétro" => "Pedro" (fuzziness); "noel" => "Noël"
        self.query['query']['multi_match']['query'] = "Pétro noel"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), ['2', '0'])


    def test_synonym(self):
        '''
        Check that synonym filter applies to both the query string and
        the indexed docs.
        '''
        # "mysterious" returns results containing "myth"/"mystery"
        # also testing stemmer: US => United States, woman => women
        self.query['query']['multi_match']['query'] = "mysterious US woman"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), ['0', '4', '1', '3'])


    def test_stemmer(self):
        '''
        Check that stemmer filter applies to both the query string and
        the indexed docs.
        '''
        # "wants" => "wanted" but not "wanna"; "fox" => "foxes"
        # also testing synonym: "quick" => "fast"
        self.query['query']['multi_match']['query'] = "She wants a quick fox"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), ['4', '3'])

        # stemmer algorithm does not work for irregulars: "slept" !=> "sleep"
        self.query['query']['multi_match']['query'] = "pretty babies slept"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), ['2', '3'])


    def test_lowercase(self):
        '''
        Check that lowercase filter applies to both the query string and
        the indexed docs
        '''
        # "us" => "US"; "SALSA" => "salsa"
        self.query['query']['multi_match']['query'] = "dance SALSA with us"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), ['2', '0', '1'])


    def test_html_stripper(self):
        '''
        Check that html stripping filter applies to both the query string and
        the indexed docs.
        '''
        # query words with html tags in the doc
        self.query['query']['multi_match']['query'] = "circus ticket"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), ['2', '4'])

        # query with html tags
        self.query['query']['multi_match']['query'] = "politician <br> \ngala\n"
        results = db.search(self.query)
        self.assertEqual(self.get_doc_list(results), ['1', '0'])


if __name__ == "__main__":
    unittest.main()
