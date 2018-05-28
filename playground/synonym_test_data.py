# Testing the synonym analyzer for event name, description, and tags
# US => United States

events = [
    {"event1": {
        "name": "Is United States doomed?",  # US => United States
        "description": "US-UK relationships on international politics",
        "tags": ["Workshop", "Discussion"],
        "cost": 5,
        "address": "hidden",
        "venue": "The Roundtable",
        "image_url": "adlkjalkwewgwiruhwow",
        "date": "Sat, May 22",
        "time": "11am",
        "link": "37hnwekhbasfkjhbasd",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event2": {
        "name": "Secrets into the adult industry",  # adult => men/women
        "description": "Shhh!",
        "tags": ["Adult", "Entertainnment"],
        "cost": 40,
        "address": "hidden",
        "venue": "The Basement",
        "image_url": "q34ouhsdfka",
        "date": "Thurs, May 7",
        "time": "10pm",
        "link": "q409hq4lkdfa",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event3": {
        "name": "White rabbits jump, brown foxes run",  # jump => hop/leap
        "description": "Explore the allegory",
        "tags": ["Theater",  "Acting"],
        "cost": 65,
        "address": "hidden",
        "venue": "The Stage",
        "image_url": "q49halkaskj",
        "date": "Sat, May 5",
        "time": "7pm",
        "link": "2hsdfkqkhsdflkhar",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event4": {
        "name": "Paleness and the hidden myth to hopping",   # pale => white
        "description": "Fun, puzzles, and riddles for men and women!",  # fun => interesting
        "tags": ["Food", "Drinks", "Show"],
        "cost": 35,
        "address": "hidden",
        "venue": "The Hall",
        "image_url": "2409haflkjar",
        "date": "Wed, May 12",
        "time": "7pm",
        "link": "q294oihsdfkaw",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event5": {
        "name": "Mystery dinner crawl and other interesting things",  # mystery => puzzle/myth/riddle
        "description": "Experience the life of a detective!",
        "tags": ["Entertainment", "Food/Drinks", "Performance Arts"],
        "cost": 55,
        "address": "hidden",
        "venue": "The Hall",
        "image_url": "09haslkbja",
        "date": "Tues, May 8",
        "time": "8pm",
        "link": "12309hsdflkj",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 }
]
