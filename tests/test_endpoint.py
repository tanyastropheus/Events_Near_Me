import unittest, sys
sys.path.append('..')
import event_app.app
from unittest.mock import patch
from pprint import pprint
import json

event = {
    "keywords": "",
    "tags": [],
    "radius": "2mi",
    "user_location": {
        "lat": 37.7749300,  #default: San Francisco
        "lng":  -122.4194200
    },
    "cost": 20,  # upper bound of cost
    "time": [],
    "date": ""
}

def DBsearch_side_effect(query):
    '''returns different values based on the input query receiveed'''
    # search for all events
    if 'constant_score' in query['query']:
        """
        print("received: Any")
        pprint(query)
        """
        return {'Music': 'a', 'Family': 'b', 'Workshop': 'c'}

    # search for event tags
    elif query['query']['bool']['must']['multi_match']['fields'] == 'tags' and\
    query['query']['bool']['should']['multi_match']['fields'] == 'name':
        """
        print("received: tags")
        pprint(query)
        """
        return {'Music': 'a', 'Family': 'b'}

    # search for event keywords
    elif query['query']['bool']['must']['multi_match']['fields'] == ['name', 'tags']:
        """
        print("received: keywords")
        pprint(query)
        """
        return {'Music': 'Beetles Anniversary'}
    else:
        return {'error': 'does not exist'}


class EventEndPoint(unittest.TestCase):
    '''testing the logic of the event search Flask endpoint'''
    def setUp(self):
        event_app.app.app.config['TESTING'] = True
        self.app = event_app.app.app.test_client()
        event['keywords'] = ""
        event['tags'] = []

    @patch('event_app.app.DB.search')
    def test_search_all(self, mock_DB_search):
        ''''Check that  "Any" event tag generates query for all events'''
        mock_DB_search.side_effect = DBsearch_side_effect

        # data sent from the front end to be parsed and queried
        event['tags'] = ["Any"]

        response = self.app.post(
            '/api/event_search',
            data=json.dumps(event),
            content_type='application/json')

        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(response.data.decode()),
                         {'Music': 'a', 'Family': 'b', 'Workshop': 'c'})


    @patch('event_app.app.DB.search')
    def test_event_tags(self, mock_DB_search):
        '''Check that selected event tags generate appropriate query'''
        mock_DB_search.side_effect = DBsearch_side_effect

        # data sent from the front end to be parsed and queried
        event['tags'] = ["Festival/Fair", "Museums", "Theater"]

        response = self.app.post(
            '/api/event_search',
            data=json.dumps(event),
            content_type='application/json')

        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(response.data.decode()),
                         {'Music': 'a', 'Family': 'b'})


    @patch('event_app.app.DB.search')
    def test_event_keywords(self, mock_DB_search):
        '''Check that event keywords generate appropriate query'''
        mock_DB_search.side_effect = DBsearch_side_effect

        # data sent from the front end to be parsed and queried
        event['keywords'] = "Beetles Concert SF"

        response = self.app.post(
            '/api/event_search',
            data=json.dumps(event),
            content_type='application/json')

        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(response.data.decode()),
                         {'Music': 'Beetles Anniversary'})


if __name__ == "__main__":
    unittest.main()
