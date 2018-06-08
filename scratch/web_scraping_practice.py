#!/usr/bin/python3
'''A playground for learning web scraping with Beautiful Soup 4'''

import requests
from bs4 import BeautifulSoup

link = 'https://www.sfstation.com/calendar'
page = requests.get(link)
soup = BeautifulSoup(page.content, 'html.parser')

# get all event titles on page 1
titles_one_page = [x.get_text() for x in soup.find_all('a', class_='url summary')]
print(titles_one_page)

# get all event links on page 1
links_one_page = [x.get('href') for x in soup.find_all('a', class_='url summary')]
print(links_one_page)
