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

class EventEndPoint(unittest.TestCase):
    '''testing the logic of the event search Flask endpoint'''
    def setUp(self):
        event_app.app.app.config['TESTING'] = True
        self.app = event_app.app.app.test_client()
        event['keywords'] = ""
        event['tags'] = []


    @staticmethod
    def DBsearch_side_effect(query):
        '''returns different values based on the input query receiveed'''
        print("query received")
        pprint(query)
        all_events = {
            'query': {
                'constant_score': {
                    'filter': {
                        'bool': {
                            'must': [
                                {'geo_distance': {
                                    'distance': "",
                                    'location': {
                                        'lat': 37.77493,
                                        'lon': -122.41942
                                    }
                                }
                             },
                                {'range': {
                                    'cost': {
                                        'gte': -1,
                                        'lte': 0
                                    }
                                }
                             }
                            ]
                        }
                    }
                }
            }
        }

        event_query = {
            'query': {
                'bool': {
                    'filter': {
                        'bool': {
                            'must': [
                                {'geo_distance': {
                                    'distance': '2mi',
                                    'location': {'lat': 37.77493,
                                                 'lon': -122.41942
                                              }
                                }
                             },
                                {'range': {
                                    'cost': {
                                        'gte': -1,
                                        'lte': 20
                                    }
                                }
                             }
                            ]
                        }
                    },
                    'must': {
                        'multi_match': {
                            'fields': ['name', 'description', 'tags'],
                            'fuzziness': 'AUTO',
                            'query': '',
                            'analyzer': 'english_synonym'
                        }
                    }
                }
            }
        }
        if 'constant_score' in query['query']:
            radius = query['query']['constant_score']['filter']['bool']['must'][0]['geo_distance']['distance']
            max_cost = query['query']['constant_score']['filter']['bool']['must'][1]['range']['cost']['lte']
            all_events['query']['constant_score']['filter']['bool']['must'][0]['geo_distance']['distance'] = radius
            all_events['query']['constant_score']['filter']['bool']['must'][1]['range']['cost']['lte'] = max_cost

        else:
            query_string = query['query']['bool']['must']['multi_match']['query']
            event_query['query']['bool']['must']['multi_match']['query'] = query_string

        # search for all events
        if query == all_events:
            return {'Music': 'a', 'Family': 'b', 'Workshop': 'c'}

            # search for event keywords
        elif query == event_query:
            return {'Music': 'Beetles Anniversary'}

        else:
            return {'error': 'does not exist'}


    def get_data(self, event):
        '''send test data from the front end to the endpoint'''
        response = self.app.post(
            '/api/event_search',
            data=json.dumps(event),
            content_type='application/json')
        return response


    @patch('event_app.app.DB.search')
    def test_search_all(self, mock_DB_search):
        ''''Check that  "Any" event tag generates query for all events'''
        mock_DB_search.side_effect = EventEndPoint.DBsearch_side_effect

        # data sent from the front end to be parsed and queried
        event['tags'] = ["Any"]

        response = self.get_data(event)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(response.data.decode()),
                         {'Music': 'a', 'Family': 'b', 'Workshop': 'c'})


    @patch('event_app.app.DB.search')
    def test_event_tags(self, mock_DB_search):
        '''Check that selected event tags generate appropriate query'''
        mock_DB_search.side_effect = EventEndPoint.DBsearch_side_effect

        # data sent from the front end to be parsed and queried
        event['tags'] = ["Festival/Fair", "Museums", "Theater"]

        response = self.get_data(event)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(response.data.decode()),
                         {'Music': 'Beetles Anniversary'})


    @patch('event_app.app.DB.search')
    def test_event_keywords(self, mock_DB_search):
        '''Check that event keywords generate appropriate query'''
        mock_DB_search.side_effect = EventEndPoint.DBsearch_side_effect

        # data sent from the front end to be parsed and queried
        event['keywords'] = "Beetles Concert SF"

        response = self.get_data(event)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(response.data.decode()),
                         {'Music': 'Beetles Anniversary'})


    @patch('event_app.app.DB.search')
    def test_cost(self, mock_DB_search):
        '''check that endpoint validates cost range input'''
        mock_DB_search.side_effect = EventEndPoint.DBsearch_side_effect
        event['tags'] = ['Any']

        event['cost'] = "100+"
        response = self.get_data(event)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(response.data.decode()),
                         {'Music': 'a', 'Family': 'b', 'Workshop': 'c'})

        event['cost'] = 0
        response = self.get_data(event)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(response.data.decode()),
                         {'Music': 'a', 'Family': 'b', 'Workshop': 'c'})

        event['cost'] = -140.45
        response = self.get_data(event)
        self.assertTrue(response.status_code == 404)

        '''should I worry about this?
        event['cost'] = 0827428
        response = self.get_data(event)
        self.assertTrue(response.status_code == 404)
        '''
        event['cost'] = "2de42&&*("
        response = self.get_data(event)
        self.assertTrue(response.status_code == 404)

        event['cost'] = 17.3987175083922340920230712370238939128349014
        response = self.get_data(event)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(response.data.decode()),
                         {'Music': 'a', 'Family': 'b', 'Workshop': 'c'})
    """

    @patch('event_app.app.DB.search')
    def test_radius(self, mock_DB_search):
        '''check that endpoint validates radius input'''
        mock_DB_search.side_effect = EventEndPoint.DBsearch_side_effect
        event['tags'] = ['Any']

        event['radius'] = "-3mi"
        response = self.get_data(event)
        self.assertTrue(response.status_code == 404)

        event['radius'] = "2.34057198340981209834098103489398734576349714mi"
        response = self.get_data(event)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(response.data.decode()),
                         {'Music': 'a', 'Family': 'b', 'Workshop': 'c'})

        event['radius'] = "0mi"
        response = self.get_data(event)
        self.assertTrue(response.status_code == 404)

        event['radius'] = "00248271mi"
        response = self.get_data(event)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(json.loads(response.data.decode()),
                         {'Music': 'a', 'Family': 'b', 'Workshop': 'c'})

        event['radius'] = "0024.8271mi"
        response = self.get_data(event)
        self.assertEqual(json.loads(response.data.decode()),
                         {'Music': 'a', 'Family': 'b', 'Workshop': 'c'})

        event['radius'] = "8ne48*%@4mi"
        response = self.get_data(event)
        self.assertTrue(response.status_code == 404)
    """

if __name__ == "__main__":
    unittest.main()
