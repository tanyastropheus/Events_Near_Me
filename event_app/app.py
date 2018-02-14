#!/usr/bin/python3

import requests
from elasticsearch import Elasticsearch
from flask import Flask, render_template
app = Flask(__name__)

# check ES is up and running
res = requests.get('http://localhost:9200')
print(res.status_code)

# connect to ES server
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

@app.route('/')
def show_all():
    search_all = requests.get('http://localhost:9200/events/_search?pretty')
    return search_all.content

@app.route('/map')
def display_map():
    return render_template('geo_detect.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
