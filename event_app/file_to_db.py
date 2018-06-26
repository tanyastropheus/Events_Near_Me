#!/user/bin/python3
'''load event data from file to Elasticserach index'''
import json
from event_app import db

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
