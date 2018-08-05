import sys
sys.path.append('..')
import unittest
from elasticsearch import Elasticsearch
from event_app.db import DB
from pprint import pprint

db = DB('test_filter', 'test_filter_doc')
class TestFilter(unittest.TestCase):
    '''
    To test the filters implemented in the custom analyzer.

    '''
    def setUp(self):
        fil = db.event_english['analysis']['analyzer']['event_english']

    def tearDown(self):
        db.delete_index()

    def test_lowercase(self):
        db.event_english['analysis']['analyzer']['event_english']['filter'] = ['lowercase']
        db.create_index()

        text = ["LGBTQ", "Food/Drinks"]
        expected = ["lgbtq", "food", "drinks"]
        self.assertCountEqual(db.get_tokens("analyzer", "event_english", text,
                                            'test_filter'), expected)

    def test_possessive(self):
        db.event_english['analysis']['analyzer']['event_english']['filter'] = ['english_possessive_stemmer']
        db.create_index()

        text = "DJ's Party!"
        expected = ["DJ", "Party"]
        self.assertCountEqual(db.get_tokens("analyzer", "event_english", text,
                                            'test_filter'), expected)

        text = "My grandma's grandmas!"
        expected = ["My", "grandma", "grandmas"]
        self.assertCountEqual(db.get_tokens("analyzer", "event_english", text,
                                            'test_filter'), expected)

    def test_abbreviation(self):
        db.event_english['analysis']['analyzer']['event_english']['filter'] = ['english_possessive_stemmer']
        db.create_index()

        text = "It's he's: we're going'.  We'll don't tell_anyone I'm"
        # tokenizer does NOT break words by '_'
        # tell_anyone => tell_anyone
        # filter treats "It's" as possessive -> "It", "he's" -> "he"
        expected = ["It", "he", "we're", "going", "We'll", "I'm", "don't", "tell_anyone"]
        self.assertCountEqual(db.get_tokens("analyzer", "event_english", text,
                                            'test_filter'), expected)


    def test_stopwords(self):
        db.event_english['analysis']['analyzer']['event_english']['filter'] = ['english_stop', 'english_possessive_stemmer']
        db.create_index()

        text = "This is the best w/o on the chef's menu walking.  Non-negotiable."
        expected = ["This", "best", "w", "o", "chef", "menu", "walking", "Non", "negotiable"]

        self.assertCountEqual(db.get_tokens("analyzer", "event_english", text,
                                            'test_filter'), expected)

    def test_accents(self):
        db.event_english['analysis']['analyzer']['event_english']['filter'] = ['asciifolding']
        db.create_index()

        fil = ['asciifolding']
        text = "Pédro, this rôle is such déjà vu.  Está loca!"
        expected = ["Pedro", "this", "role", "is", "such", "deja", "vu",
                    "Esta", "loca"]
        self.assertCountEqual(db.get_tokens("analyzer", "event_english", text,
                                            'test_filter'), expected)


    def test_stemmer(self):
        db.event_english['analysis']['analyzer']['event_english']['filter'] = ['english_stemmer', 'lowercase', 'english_stop']
        db.create_index()

        text = "The pigs kissed Sleeping Beauty and woke her.  She hates\
        mysteries/tomatoes."
        expected = ["pig", "kiss", "sleep", "beauti", "woke",
                    "her", "she", "hate", "mysteri", "tomato"]

        self.assertCountEqual(db.get_tokens("analyzer", "event_english", text,
                                            'test_filter'), expected)


    def test_char_filter(self):
        '''test that char filter will strip "\n" at the end'''
        db.event_english['analysis']['analyzer']['event_english']['filter'] = ['english_possessive_stemmer']
        db.event_english['analysis']['analyzer']['event_english']['char_filter'] = ['html_strip']
        db.create_index()

        text = "Bitter Melon\nOrigin Story\nAunt Lily’s (Closing Night)\n\n\n"
        expected = ["Bitter", "Melon", "Origin", "Story", "Aunt", "Lily", "Closing", "Night"]
        self.assertEqual(db.get_tokens("analyzer", "event_english", text,
                                            'test_filter'), expected)

        text = "Simpson's show \"You Look Nice Today\" has received"
        expected = ["Simpson", "show", "You", "Look", "Nice", "Today", "has", "received"]
        self.assertEqual(db.get_tokens("analyzer", "event_english", text,
                                            'test_filter'), expected)

        print("char filter:", db.get_tokens("analyzer", "event_english", text, 'test_filter'))

if __name__ == "__main__":
    unittest.main()
