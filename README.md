# Events Near Me

A web application that lets the user search events by keywords or category, and filter by distance, cost, and time. 

**Demo site**: <http://eventsnearme.fun>

*Currently contains **_only events in the Bay Area_**

![alt text](https://i.imgur.com/BmU6dzT.png)

## Getting Started
### Architecture
![alt text](https://i.imgur.com/awzPV2w.png)

### Prerequisites

* Python 3. 4. 3
* Elasticsearch version 6. 2. 0.  Follow this [guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-14-04) for installation and configuration

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


## Running the tests

Explain how to run the automated tests for this system

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

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

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
