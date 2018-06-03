# Test if the analyzer tokenizes by non-letters for name, description, and tags
# dog's => dog, s
# and/or => and, or
# ever-lasting => ever, lasting

[
    {"event1": {
        # DJ's => DJ, s
        "name": "DJ's Party!",
        # can also check synonym:  U.S. => United States/US
        "description": "Come party with the finest DJ's from the U.S.!",
        "tags": ["Dance", "Music", "Club"],
        "cost": 45,
        "address": "hidden",
        "venue": "The Nightingale's",
        "image_url": "alkjanskd",
        "date": "Fri, May 27",
        "time": "10pm",
        "link": "vskjpwps",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event2": {
        # can also check synonym: Grandma => grandmother
        # Grandma's => Grandma, s
        "name": "Celebrating Grandma's 101st Birthday!",
        "description": "How many people live up to 101 like grandma?!",
        "tags": ["Family/Children", "Community", "Food/Drinks"],
        "cost": 0,
        "address": "hidden",
        "venue": "Berkeley Community Center",
        "image_url": "lkjai",
        "date": "Fri, May 20",
        "time": "2pm - 5pm",
        "link": "93usfkjnwl1",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event3": {
        # He/She => He, She
        "name": "He/She - the pronoun dilemma",
        "description": "Join us to learn how to properly address someone.",
        "tags": ["Workshop", "Discussion", "LGBTQ"],
        "cost": 10,
        "address": "hidden",
        "venue": "The Place",
        "image_url": "ljnt0ioxcslr",
        "date": "Tues, May 31",
        "time": "9am",
        "link": "sfljne09df-ksadj",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event4": {
        # dog's => dog, s
        "name": "This is the time of dogs",
        "description": "heaven - treats, dates, everything",
        "tags": ["Animal", "Family/Children"],
        "cost": 35,
        "address": "hidden",
        "venue": "The Park",
        "image_url": "alkjnslkjnww4928v",
        "date": "Sat, May 21",
        "time": "11am - 5pm",
        "link": "0923oiaskjajgeuihqr",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event5": {
        # Art-related => Art, related
        "name": "Art-related, fun-filled Evening!",
        # inner-self => inner, self
        "description": "Come discover your inner-self and inner-artist!",
        "tags": ["Arts/Performance", "Drinks"],
        "cost": 85,
        "address": "hidden",
        "venue": "The Gallery",
        "image_url": "aljnsqwe9asdghw85",
        "date": "Wed, May 13",
        "time": "6pm-8pm",
        "link": "salkjnalkjns",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 },
    {"event6": {
        "name": "Three Little Pigs",
        # White's => White, s
        # can also check stemmer: dwarf => dwarfs
        "description": "Whatever happened to the three little pigs and Snow White's dwarfs?",
        "tags": ["Literacy", "Story-Telling"],
        "cost": 0,
        "address": "hidden",
        "venue": "The Children's Museum",
        "image_url": "apoij-30ijdfd",
        "date": "Thurs, May 27",
        "time": "4pm",
        "link": "2p0jaasgjnPUON",
        "location": {
            "lat": 0.0,
            "lon": 0.0
        }
    }
 }
]
