#!/usr/bin/env python3
import datetime
import warnings
import os
from urllib.parse import urlparse
import re
import json
import itertools
from time import sleep
from random import normalvariate
from is_date_range import is_date_range, dates, month
import dateutil.parser
import logging

import sqlite3

import requests
import parsedatetime as pdt
cal = pdt.Calendar()
import lxml.html
import threading

logger = logging.getLogger('undervalued-sublets')

from cache import get

try:
    from config import apikey, locations
except ImportError:
    logger.critical('You must specify the "apikey" and "locations" in config.py.')
    exit(1)

try:
    from config import http_proxy, http_proxy_username, http_proxy_username, http_proxy_password
    proxies = {'http':'http://' + http_proxy}
    auth = requests.auth.HTTPProxyAuth(http_proxy_username, http_proxy_password)
except ImportError:
    proxies = None

def main():
    for location in locations:
        t = threading.Thread(target = search_location, args = (apikey, location))
        t.start()

def search_location(apikey, location, parse = False):
    s = search3Taps(apikey, location)
    finished_pages = set(row[0] for row in s.cursor.execute('SELECT url from results').fetchall())
    for listing in s:
        page = listing['external_url']

        if page not in finished_pages:

            if not parse:
                # Just download the page
                loadCraigslist(page)
                continue

            html = lxml.html.fromstring(loadCraigslist(page).read())
            if is_date_range(html):
                start, end = tuple(map(month, dates(html)))
            else:
                start = end = None
            text = html.text_content()
            data = {
                'url': listing['external_url'],

                # From 3taps
                'heading': listing['heading'],
                'long': listing['location']['long'],
                'lat': listing['location']['lat'],
                'zipcode': listing['location']['zipcode'],
                'address': listing['location'].get('formatted_address', ''),

                # From my parse
                'price': listing.get('price', price(text)),
                'start': start,
                'end': end,
                'furnished': furnished(text),
                'posted': craigsdate('posted: ', html),
                'updated': craigsdate('updated: ', html),
                'weekly': weekly(html),

            }
            # Special for certain times of year
            for thing in ['superbowl', 'sxsw']:
                data[thing] = thing in text.lower().replace(' ', '')
            s.save_dict('results', data)
            s.connection.commit()

# http://docs.3taps.com/reference_api.html
levels = {
    'country',
    'state',
    'metro',
    'region',
    'county',
    'city',
    'locality',
    'zipcode',
}
class Search:
    def __init__(self, subdomain):
        self.subdomain = subdomain
        self.buffer = []
        self.search_url = 'https://%s/sub/index000.html' % subdomain

    def __next__(self):
        if len(self.buffer) > 0:
            return self.buffer.pop(0)


        if self.html.xpath('count(//p[@class="row"])') == 0:
            raise StopIteration

    def download(self):
        fp = get(self.search_url)
        html = lxml.html.fromstring(fp.read())
        html.make_links_absolute(self.search_url)

        nexts = set(self.html.xpath('//a[contains(text(),"next >")]/@href')))
        if len(nexts) != 1:
            raise ValueError('No next page for %s' % self.search_url)

        # Add listings
        self.buffer.extend(map(str,html.xpath('//p[@class="row"]/a/@href')))

        # Bump search url
        self.search_url = str(list(nexts)[0])

def price(text):
    'Find the price of a listing. Use the highest dollar value in the listing.'
    numbers = re.findall(r'[$0-9]+', re.sub(r'[, ]', '', text))
    monies = filter(lambda x: '$' in x, numbers)
    integers = list(_ints(money.replace('$','') for money in monies))
    if len(integers) > 0:
        return max(integers)

def furnished(text):
    return 'furnished' in text and not 'unfurnished' in text

def _ints(monies):
    for money in monies:
        try:
            yield int(money)
        except ValueError:
            pass

def craigsdate(text, html):
    ds = html.xpath('//p[text()="%s"]/time/@datetime' % text)
    if ds != []:
        e = dateutil.parser.parse(ds[0])
        return int(datetime.datetime.astimezone(e).timestamp())

def weekly(html):
    return 'week' in html.text_content()

if __name__ == '__main__':
    main()
