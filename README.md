# Events Near Me

A web application that lets users search events of the day by keywords or category, and filter by distance, cost, and time. 

**Demo site**: <http://eventsnearme.fun>

*Currently contains **_only events in the Bay Area_**

![alt text](https://i.imgur.com/BmU6dzT.png)

## Table of Contents

- [Built With](#built-with)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Running the tests](#running-the-tests)
- [Deployment](#deployment)
- [Known Bugs](#knownbugs)
- [Future Development](#future-development)
- [Author](#author)


## Features
* **Full text search**: 
with event keywords (*AND*: returns events that meet all keywords criteria)

* **Search-as-you-type**: 
with event keywords (returns events that contain the keyword *anywhere in the title*)

* **Exact search**: 
with event categories (*OR*: returns events that meet at least one category)

## Built With

* [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web Scraping Tool
* [Elasticsearch](https://www.elastic.co/) - Document store and Search Engine
* [Flask](http://flask.pocoo.org/) - Web Framework

### Architecture
* *To be implemented*: Obtaining event data from EventBrite
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

   We are using the low-level Python Elasticsearch Client to interface with Elasticsearch.  Here is the [documentation](https://elasticsearch-py.readthedocs.io/en/master/) and [source code](https://elasticsearch-py.readthedocs.io/en/master/).
   ```
   pip3 install -r /Events_Near_Me/requirements.txt
   ```

3. Create a *local_setting.py* file that handles the Flask debugging setting in ```Events_Near_Me/event_app/``` directory.  It will be set to ```debug = True``` in development, and ```debug = False``` in production.  Below is an example:

   ```
   #!/usr/bin/python3
   '''
   change Flask debug setting based on locality (development/production)
   '''
   debug = False
   ```

## Usage

### Getting Live Event Data

1. Start the Elasticsearch Server:
   ```
   sudo service elasticsearch start
   ```

2. Run the web scraper to get event data of the day.  The events will be saved in the ```events_today``` index with ```info``` as the document type.
   ```
   cd Events_Near_Me
   ./sf_station_scrape.py
   ```

3. Start Flask application server.  To accommodate the spawning of child processes when debugger is set to True in development, we need to specify the ```PYTHONPATH```:
   ```
   PYTHONPATH=`pwd` python3 -m event_app.app
   ```

### Load Event Data from File
One may also load event data from a file instead of obtaining live events from running the web scraper.  The ```tests/test_data``` directory provides sample test data sets.  To do so, replace **Step 2** above with the follow the steps:

1.  Create the index ```example_test_index``` with a doc_type ```example_test_doc``` to store file data and specify the file ```tests/test_data/test_data.txt``` where data is to be loaded.  Have Flask serve the data from file for the web application:
   ```
   PYTHONPATH=`pwd` INDEX='example_test_index' DOCTYPE='example_test_doc' FILE='tests/test_data/test_data.txt' python3 -m event_app.app
   ```

2. To delete the test index:

   Set environmental variable ```DELETE='true'```:
   ```
   PYTHONPATH=`pwd` INDEX='example_test_index' DOCTYPE='example_test_doc' DELETE='true'  python3 -m event_app.app
   ```

   Or use the Elasticsearch API:

   ```
   curl -X DELETE 'localhost:9200/example_test_index'
   ```

## Running the tests

The unit tests are focused on ensuring the proper data is returned in response to the user's event search criteria.

| Test                                                  | Purpose                                                                                                      |
|:------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------|
| *test_tokenizer.py*, *test_filters.py*                | Ensure that the indexing strategies are properly implemented through customed field mapping in Elasticsearch |
| *test_full_text_search.py*, *test_compound_search.py* | Check that queries are properly implemented and returns the correct results                                  |
| *test_endpoint.py*                                    | Test that endpoint logic is correct                                                                          |

**Example:**

```
python3 -m unittest tests/test_tokenizer.py
```

## Deployment

This project was deployed to a Ubuntu 14.04 server, with [Nginx](https://www.nginx.com) as the web server and [Gunicorn](http://gunicorn.org) as the Web Server Gateway Interface (WSGI) between Flask and Nginx.  The processes are managed by [Supervisor](http://supervisord.org/introduction.html). Here is a [nice reference guide](https://realpython.com/kickstarting-flask-on-ubuntu-setup-and-deployment/) that describes the deployment using these technologies.

## Known Bugs

1. Marker display does not get updated when checking/unchecking time slots of the day

2. Selecting multiple event categories does not accurately display the events that meet one or more category criteria

3. Code does not pass some test cases (*test_full_text_search.py*, *test_compound_search.py*, *test_endpoint.py*)


## Future Development

1. Fix marker display when time slot is checked/unchecked

2. Implement terms search instead of full-text search for accurate event category (OR) results

3. Update test cases to reflect the change in endpoint logic and implementation on time selection

4. Aggregate more data from event sites (e.g. EventBrite, SF funcheap, ...etc)

5. Add calendar feature that allows the user to search events on a given date

6. Make event API available for the public

7. Allow the user to submit events

8. Add events for other regions


## Author

**Tanya Kryukova** - [LinkedIn](https://www.linkedin.com/in/tanya-kryukova) / [Twitter](https://twitter.com/tyastropheus)
