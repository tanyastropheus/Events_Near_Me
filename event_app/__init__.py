#!/usr/bin/python3
'''select the event index to query events from'''

from time import sleep
from event_app.db import DB
from os import getenv

# create/select index to load events from
index = getenv('INDEX')
doc_type = getenv('DOCTYPE')
db = DB(index, doc_type)

if getenv('DELETE') == 'false':
    db.create_index()
elif getenv('DELETE') == 'true':
    db.delete_index()

# option to load data from file
if getenv('FILE'):
    filename = getenv('FILE')
    events = load_data_from_file(filename)
    store_docs(events)

    # allow time for Elasticsearch server to store all data
    sleep(3)

    # look up & save geolocation to db based on address
    num_docs = db.get_num_docs()
    for i in range(num_docs):
        geo = db.addr_to_geo(i)
        db.save_geo(i, geo)
        i += 1

    # allow time for Elasticsearch server to store all data
    sleep(3)
