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
    def tearDown(self):
        db.delete_index()

    def test_lowercase(self):
        db.english_synonym['analysis']['analyzer']['english_synonym']['filter'] = ['lowercase']
        db.create_index()

        text = ["LGBTQ", "Food/Drinks"]
        expected = ["lgbtq", "food", "drinks"]
        self.assertCountEqual(db.get_tokens("analyzer", "english_synonym", text,
                                            'test_filter'), expected)

    def test_possessive(self):
        db.english_synonym['analysis']['analyzer']['english_synonym']['filter'] = ['english_possessive_stemmer']
        db.create_index()

        text = "DJ's Party!"
        expected = ["DJ", "Party"]
        self.assertCountEqual(db.get_tokens("analyzer", "english_synonym", text,
                                            'test_filter'), expected)

        text = "My grandma's grandmas!"
        expected = ["My", "grandma", "grandmas"]
        self.assertCountEqual(db.get_tokens("analyzer", "english_synonym", text,
                                            'test_filter'), expected)

        text = "It's me: I'm just chillin'.  Plz don't tell_anyone"
        # filter treats "It's" as possessive => "It"
        expected = ["It", "me", "I'm", "just", "chillin", "Plz", "don't",
                    "tell_anyone"]
        self.assertCountEqual(db.get_tokens("analyzer", "english_synonym", text,
                                            'test_filter'), expected)

    def test_stopwords(self):
        db.english_synonym['analysis']['analyzer']['english_synonym']['filter'] = ['english_stop', 'english_possessive_stemmer']
        db.create_index()

        text = "This is the best w/o on the chef's menu walking.  Non-negotiable."
        expected = ["This", "best", "w", "o", "chef", "menu", "walking", "Non", "negotiable"]

        self.assertCountEqual(db.get_tokens("analyzer", "english_synonym", text,
                                            'test_filter'), expected)

    def test_accents(self):
        db.english_synonym['analysis']['analyzer']['english_synonym']['filter'] = ['asciifolding']
        db.create_index()

        fil = ['asciifolding']
        text = "Pédro, this rôle is such déjà vu.  Está loca!"
        expected = ["Pedro", "this", "role", "is", "such", "deja", "vu",
                    "Esta", "loca"]
        self.assertCountEqual(db.get_tokens("analyzer", "english_synonym", text,
                                            'test_filter'), expected)


    def test_stemmer(self):
        db.english_synonym['analysis']['analyzer']['english_synonym']['filter'] = ['english_stemmer', 'lowercase', 'english_stop']
        db.create_index()

        text = "The pigs kissed Sleeping Beauty and woke her.  She hates\
        mysteries/tomatoes."
        expected = ["pig", "kiss", "sleep", "beauti", "woke",
                    "her", "she", "hate", "mysteri", "tomato"]

        self.assertCountEqual(db.get_tokens("analyzer", "english_synonym", text,
                                            'test_filter'), expected)

    def test_synonym(self):
        db.english_synonym['analysis']['analyzer']['english_synonym']['filter'] = ['synonym']
        db.create_index()

        text = "baby"
        expected = "baby"

        # should save other synonyms
        self.assertNotEqual(db.get_tokens("analyzer", "english_synonym", text,
                                            'test_filter'), expected)
        print("Synonyms:", db.get_tokens("analyzer", "english_synonym", text, 'test_filter'))

if __name__ == "__main__":
    unittest.main()
