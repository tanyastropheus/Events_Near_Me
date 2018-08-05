# Events Near Me

A web application that lets the user search events of the day by keywords or category, and filter by distance, cost, and time. 

**Demo site**: <http://eventsnearme.fun>

*Currently contains **_only events in the Bay Area_**

![alt text](https://i.imgur.com/BmU6dzT.png)

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
We are using the low-level Python Elasticsearch Client to interface with Elasticsearch.  Here is the [documentation](https://elasticsearch-py.readthedocs.io/en/master/) and [source code](https://elasticsearch-py.readthedocs.io/en/master/)

3. Create a *local_setting.py* file that handles the Flask debugging setting in ```Events_Near_Me/event_app/``` directory.  It will be set to ```debug = True``` in development, and ```debug = False``` in production.  Below is an example:

```
#!/usr/bin/python3
'''
change Flask debug setting based on locality (development/production)
'''
debug = False
```

### Usage

1. Start the Elasticsearch Server:
```
sudo service elasticsearch start
```

2. Run the web scraper to get events data:
```
cd Events_Near_Me
./sf_station_scrape.py
```

3. Start Flask application server.  To accommodate the spawning of child processes when debugger is set to True in development, we need to specify the ````PYTHONPATH```:
* In development:
```
PYTHONPATH=`pwd` python3 -m event_app.app
```
* In production:
```
python3 -m event_app.app
```

## Running the tests

The unit tests are focused on ensuring the proper data is returned in response to the user's event search criteria.

| Test                                                  | Purpose                                                                                                      |
| ------------------------------------------------------|:------------------------------------------------------------------------------------------------------------:|
| *test_tokenizer.py*, *test_filters.py*                | Ensure that the indexing strategies are properly implemented through customed field mapping in Elasticsearch |
| *test_full_text_search.py*, *test_compound_search.py* | Check that queryes are properly implemented and returns the correct results                                  |
| *test_endpoint.py*                                    | Test that endpoint logic is correct                                                                          |


### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Known Bugs

## Future Development

## Deployment

Add additional notes about how to deploy this on a live system


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
