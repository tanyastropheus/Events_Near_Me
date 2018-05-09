#!/usr/bin/python3
'''Playing with python elasticsearch low level client'''
import requests, json
from pprint import pprint
from elasticsearch import Elasticsearch

# check ES is up and running
res = requests.get('http://localhost:9200')
#print(res.content)

# connect to ES server
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# iterate over swapi people documents and index them
r = requests.get('http://localhost:9200')
'''
i = 1
while r.status_code == 200:
    r = requests.get('http://swapi.co/api/people/'+ str(i))
    es.index(index='sw', doc_type='people', id=i, body=json.loads(r.text))
    i += 1

print(i)
'''
#pprint(es.get(index='sw', doc_type='people', id=5))
#pprint(es.search(index="sw", body={"query": {"match": {'name':'Darth Vader'}}}))

pprint(es.search(index="sw", body={"query": {"prefix": {'name':'lu'}}}))
