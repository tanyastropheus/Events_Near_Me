# Events Near Me

A web application that lets the user search events of the day by keywords or category, and filter by distance, cost, and time. 

**Demo site**: <http://eventsnearme.fun>

*Currently contains **_only events in the Bay Area_**

![alt text](https://i.imgur.com/BmU6dzT.png)

## Table of Contents

- [Built With](#built-with)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Running the tests](#running-the-tests)
- [Known Bugs](#knownbugs)
- [Future Development](#future-development)
- [Author](#author)
- [Acknowledgements](#acknowledgements)


## Built With

* [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web Scraping Tool
* [Elasticsearch](https://www.elastic.co/) - Document store and Search Engine
* [Flask](http://flask.pocoo.org/) - Web Framework

### Architecture
![alt text](https://i.imgur.com/awzPV2w.png)

## Getting Started

### Prerequisites

* Python 3
* Elasticsearch version 6.2.0.  Follow [this guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-14-04) for installation and configuration

### Installing

1. Clone the repository
```
git clone https://github.com/tanyastropheus/Events_Near_Me.git
```

2. Install required Python packages
```
pip3 install -r /Events_Near_Me/requirements.txt
```
We are using the low-level Python Elasticsearch Client to interface with Elasticsearch.  Here is the [documentation](https://elasticsearch-py.readthedocs.io/en/master/) and [source code](https://elasticsearch-py.readthedocs.io/en/master/).

3. Create a *local_setting.py* file that handles the Flask debugging setting in ```Events_Near_Me/event_app/``` directory.  It will be set to ```debug = True``` in development, and ```debug = False``` in production.  Below is an example:

```
#!/usr/bin/python3
'''
change Flask debug setting based on locality (development/production)
'''
debug = False
```

### Usage

#### Getting Live Event Data

1. Start the Elasticsearch Server:
```
sudo service elasticsearch start
```

2. Run the web scraper to get event data of the day:
```
cd Events_Near_Me
./sf_station_scrape.py
```

3. Start Flask application server.  To accommodate the spawning of child processes when debugger is set to True in development, we need to specify the ```PYTHONPATH```:

* In development:
```
PYTHONPATH=`pwd` python3 -m event_app.app
```
* In production:
```
python3 -m event_app.app
```

#### Load Event Data from File
One may also load event data from a file instead of obtaining live events from running the web scraper.  The ```tests/test_data``` directory provides sample test data sets.  To do so, replace **Step 2** above with the follow the steps:

1.  Create the index ```test_index``` with the doct_type ```test_doc``` to store file data and specify the file ```tests/test_data/test_data.txt``` where data is to be loaded.  Have Flask serve the data from file for the web application:

```
PYTHONPATH=`pwd` INDEX='test_index' DOCTYPE='test_doc' DELETE='false' FILE='tests/test_data/test_data.txt' python3 -m event_app.app
```

2. To delete the test index:

```
PYTHONPATH=`pwd` INDEX='test_index' DOCTYPE='test_doc' DELETE='false'  python3 -m event_app.app
```
or use the Elasticsearch API:

```
curl -X DELETE 'localhost:9200/test_index'
```

## Running the tests

The unit tests are focused on ensuring the proper data is returned in response to the user's event search criteria.

| Test                                                  | Purpose                                                                                                      |
|-------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------|
| *test_tokenizer.py*, *test_filters.py*                | Ensure that the indexing strategies are properly implemented through customed field mapping in Elasticsearch |
| *test_full_text_search.py*, *test_compound_search.py* | Check that queries are properly implemented and returns the correct results                                  |
| *test_endpoint.py*                                    | Test that endpoint logic is correct                                                                          |

**Example:**

```
python3 -m unittest tests/test_tokenizer.py
```

## Known Bugs

* some tests don't pass (specify those test files)
* time selection button does not update when user unchecks the time slot
* refine event category results

## Future Development

* fix bugs (by....)
* get data from more event sites (e.g. EventBrite)
* add calendar feature so user can specify event date
* make API available for public
* add SSL certificate

## Deployment

Add additional notes about how to deploy this on a live system

## Author

**Tanya Kryukova** - [LinkedIn](https://www.linkedin.com/in/tanya-kryukova) / [Twitter](https://twitter.com/tyastropheus)

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
