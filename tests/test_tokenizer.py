import sys
sys.path.append('..')
print(sys.path)
import unittest
from elasticsearch import Elasticsearch
from event_app.db import DB

db = DB('test_tokenizer', 'test_doc')

class TestTokenizer(unittest.TestCase):
    '''
    To test and understand the implementation of ElasticSearch built-in
    standard tokenizer for the web app.

    From the documentation:
        "The standard tokenizer provides grammar based tokenization (based on
    the Unicode Text Segmentation algorithm, as specified in Unicode Standard
    Annex #29"

    '''
    def test_possessive(self):
        text = "DJ's Party!"
        expected = ["DJ's", "Party"]
        self.assertCountEqual(db.get_tokens("tokenizer", "standard", text), expected)

        text = "My grandma's birthday!"
        expected = ["My", "grandma's", "birthday"]
        self.assertCountEqual(db.get_tokens("tokenizer", "standard", text), expected)

    def test_abbreviation(self):
        text = "It's me: we're going'.  We'll don't tell_anyone I'm"
        # tokenizer does NOT break words by '_'
        # tell_anyone => tell_anyone
        expected = ["It's", "me", "we're", "We'll", "going", "I'm", "don't", "tell_anyone"]
        self.assertCountEqual(db.get_tokens("tokenizer", "standard", text), expected)

    def test_nonletter(self):
        text = "self-fulfilling 'dream' - the **BEST** bitter_sweet [cake] ever+++"
        # tokenizer breaks words by '-'
        expected = ["self", "fulfilling", "dream", "the", "BEST", "bitter_sweet",
                    "cake", "ever"]
        self.assertCountEqual(db.get_tokens("tokenizer", "standard", text), expected)

        text = ['Food/Drinks', 'Discussion(hands-on)']

        expected = ["Food", "Drinks", "Discussion", "hands", "on"]
        self.assertCountEqual(db.get_tokens("tokenizer", "standard", text), expected)

    def test_ordinal(self):
        text = "The 101st anniversary (dinner-for-2!)"
        expected = ["The", "101st", "anniversary", "dinner", "for", "2"]
        self.assertCountEqual(db.get_tokens("tokenizer", "standard", text), expected)

    def test_odd_spelling(self):
        text = "Shhhh!!  Gotta be the lonnnngest day"
        expected = ["Shhhh", "Gotta", "be", "the", "lonnnngest", "day"]
        self.assertCountEqual(db.get_tokens("tokenizer", "standard", text), expected)

    def test_empty(self):
        text = ""
        expected = ""
        self.assertCountEqual(db.get_tokens("tokenizer", "standard", text), expected)

if __name__ == "__main__":
    unittest.main()
