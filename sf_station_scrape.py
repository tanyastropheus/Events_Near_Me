#!/usr/bin/python3
'''scraping event details from sfstation.com'''

import requests
import re
from bs4 import BeautifulSoup

url = 'https://www.sfstation.com/'
calendar = url + 'calendar/'
page = requests.get(calendar)
soup = BeautifulSoup(page.content, 'html.parser')
events = []

while soup.select('div#listingPagination > a')[-1].get_text() == 'Next »':
    event = {}
    event['name'] = soup.find('a', class_='url summary').get_text()
    event['link'] = url + soup.find('a', class_='url summary').get('href')

    # following event link to get additional event info
    event_url = event['link']
    event_page = requests.get(event_url)
    event_soup = BeautifulSoup(event_page.content, 'html.parser')
    if event_soup.find('dt', text=re.compile(r'When')):
        date = re.match('^[^(]+', event_soup.find('dd').get_text())
        event['date'] = date.group(0).strip()
    if event_soup.find('span', class_='address'):
        location = event_soup.find('span', class_='address').text
        event['location'] = location
    if event_soup.find('dt', text=re.compile(r'Time')):
        time= event_soup.find('dt', text=re.compile(r'Time')).next_sibling.next_sibling
        event['time'] = time.text
    if event_soup.find('dt', text=re.compile(r'Cost')):
        cost_str= event_soup.find('dt', text=re.compile(r'Cost')).next_sibling.next_sibling
        cost = re.search('\d+', cost_str.text)
        event['cost'] = int(cost.group(0))
    if event_soup.find('dt', text=re.compile(r'Tags')):
        tags = event_soup.find('dt', text=re.compile(r'Tags')).next_sibling.next_sibling
        event['tags'] = tags.text.strip().split(', ')

    events.append(event)

    next_page = url + soup.select('div#listingPagination > a')[-1].get('href')
    page = requests.get(next_page)
    soup = BeautifulSoup(page.content, 'html.parser')

    print(event)

print(events)
