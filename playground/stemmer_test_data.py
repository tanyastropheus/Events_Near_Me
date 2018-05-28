# Testing the stemmer in the analyzer for event name, description, and tags
# sleep => slept
# fox => foxes
# history => historians or historians => historian


events = [
    {"event1": {
        "name": "Three Little Pigs that jump over the fence",  # pigs => pig
        "description": "The phrase that paid",  # paid => pay
        "tags": ["Children", "Family", "Literacy"],
        "cost": 0,
        "address": "hidden",
        "venue": "The Children's Museum",
        "image_url": "49ajsdjkqgjkaf",
        "date": "Thurs, May 18",
        "time": "4pm",
        "link": "4japjnljkn2ljngasd",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event2": {
        "name": "Wanna make money waitressing?",  # wanna  => want; waitressing => waitress
        "description": "Paying customers, Listen up!",  # listen => hear, paying => pay
        "tags": ["Lecture/Workshop", "Discussion"],
        "cost": 0,
        "address": "hidden",
        "venue": "The Roundtable",
        "image_url": "[asdfmlkjnwelksfd",
        "date": "Mon, May 22",
        "time": "11am",
        "link": "29jaljnawlkjnd",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event3": {
        "name": "For budding gardener who wants to dig deeper",  # wants => want
        # leaves => leaf; foxes => fox; tree => trees; ate => eat; grew => grow
        "description": "Leaves, foxes, trees, and anything that ate and grew",
        "tags": ["Outdoors", "Gardening"],
        "cost": 25,
        "address": "hidden",
        "venue": "The Nursery",
        "image_url": "2908jfslkjnaslkjsn",
        "date": "Sun, May 28",
        "time": "10am",
        "link": "2pjaspj1kjsdfw",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event4": {
        "name":  "Sleeping beauty and me",  # Sleeping => sleep; me => I/my
        # eats => eat; hates => hate
        # can also test synonym: hate => dislike/loathe
        "description": "His mom eats pig and hates Disney",
        "tags": ["Discussion/Workshop"],
        "cost": 5,
        "address": "hidden",
        "venue": "The Roundtable",
        "image_url": "3-0janasd;lkmsa",
        "date": "Wed, May 30",
        "time": "3pm",
        "link": "asdpojpofalnjasd",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event5": {
        "name": "Those creatures that once walked and slept the Earth",  # walked => walk; slept => sleep
        "description": "Discover nature's secrets from natural historians.  Fast!",
        "tags": ["Nature", "Museum", "Workshop"],
        "cost": 30,
        "address": "hidden",
        "venue": "The Natural History Museum",
        "image_url": "wz3jnklkjnnas",
        "date": "Tues, May 2",
        "time": "2pm",
        "link": "q9jdsfljnLKJNDFA",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 }
]
