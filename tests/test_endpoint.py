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
        all_events = {
            'query': {
                'constant_score': {
                    'filter': {
                        'bool': {
                            'must': [
                                {'geo_distance': {
                                    'distance': '2mi',
                                    'location': {
                                        'lat': 37.77493,
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
                }
            }
        }
    }

        event_tags = {
            'query': {
                'bool': {
                    'filter': {
                        'bool': {
                            'must': [
                                {'geo_distance': {
                                    'distance': '2mi',
                                    'location': {
                                        'lat': 37.77493,
                                        'lon': -122.41942}}},
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
                            'fields': 'tags',
                            'fuzziness': 'AUTO',
                            'query': 'Festival/Fair Museums Theater',
                            'type': 'best_fields'
                        }
                    },
                    'should': {
                        'multi_match': {
                            'fields': 'name',
                            'fuzziness': 'AUTO',
                            'query': 'Festival/Fair Museums Theater',
                            'type': 'best_fields'
                        }
                    }
                }
            }
        }

        event_keywords = {
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
                            'fields': ['name', 'tags'],
                            'fuzziness': 'AUTO',
                            'query': 'Beetles Concert SF',
                            'type': 'best_fields'
                        }
                    }
                }
            }
        }

        # search for all events
        if query == all_events:
            return {'Music': 'a', 'Family': 'b', 'Workshop': 'c'}

        # search for event tags
        elif query == event_tags:
            return {'Music': 'a', 'Family': 'b'}

            # search for event keywords
        elif query == event_keywords:
            return {'Music': 'Beetles Anniversary'}

        else:
            return {'error': 'does not exist'}


    @patch('event_app.app.DB.search')
    def test_search_all(self, mock_DB_search):
        ''''Check that  "Any" event tag generates query for all events'''
        mock_DB_search.side_effect = EventEndPoint.DBsearch_side_effect

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
        mock_DB_search.side_effect = EventEndPoint.DBsearch_side_effect

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
        mock_DB_search.side_effect = EventEndPoint.DBsearch_side_effect

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
