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
import dateutil

import sqlite3

import requests
import parsedatetime.parsedatetime as pdt
cal = pdt.Calendar()
import lxml.html
import threading

try:
    from config import apikey, locations
except ImportError:
    print('You must specify the "apikey" and "locations" in config.py.')
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

def search_location(apikey, location):
    s = search3Taps(apikey, location)
    finished_pages = set(row[0] for row in s.cursor.execute('SELECT url from results').fetchall())
    for page in s:
        if page not in finished_pages:
            html = lxml.html.fromstring(loadCraigslist(page))
            if is_date_range(html):
                start, end = tuple(map(month, dates(html)))
            else:
                start = end = None
            text = html.text_content()
            s.cursor.execute('''
                INSERT OR REPLACE INTO results
                  (url, price, start, end, furnished, posted, updated)
                VALUES (?,?,?,?,?,?,?)''',
                (page,price(text), start, end, furnished(text), craigsdate('Posted: ', html), craigsdate('Updated: ', html)))
            s.connection.commit()

def randomsleep(mean = 1, sd = 0.5):
    "Sleep for a random amount of time"
    seconds=normalvariate(mean, sd)
    if seconds>0:
        sleep(seconds)

def loadCraigslist(craigslistUrl):
    httpCraigslistUrl = 'http://' + craigslistUrl.replace(r'^https?://','')
    parsedUrl = urlparse(craigslistUrl)
    requestUrl = 'http://' + re.sub(r'http://', '', httpCraigslistUrl)
    fileName = 'craigslist/' + parsedUrl.hostname.replace(r'\..*$', '') + parsedUrl.path;

    if not os.path.exists(fileName):
        print('Downloading to ./%s' % fileName)
        try:
            os.makedirs(re.sub(r'\/[^\/]*$', '', fileName))
        except OSError:
            pass

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0"
        }

        response = requests.get(requestUrl, headers = headers, proxies = proxies, auth = auth)
        open(fileName, 'w').write(response.text)
        randomsleep()
    return open(fileName).read()

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
class search3Taps:
    def __init__(self, apikey, location, rpp = 100, only_first_tier = False, min_price = 200, max_price = 1500):
        self.only_first_tier = only_first_tier
        level, value = location
        if level not in levels:
            raise ValueError('"level" must be one of %s.' % ', '.join(levels))
        args = {
            'apikey':apikey,
            'rpp':rpp,
            'min_price':min_price,
            'max_price':max_price,
            'level': level,
            'value': value,
            'body':'~bnb.com',
        }
        self.apiUrl = "http://search.3taps.com?auth_token=%(apikey)s&SOURCE=CRAIG&location.%(level)s=%(value)s&category=RSUB&retvals=external_url&rpp=%(rpp)d&price=%(min_price)s..%(max_price)d&body=%(body)s" % args
        self.date = datetime.date.today()
        print(self.apiUrl)

        self.connection = sqlite3.connect('craigslist.sqlite')
        self.cursor = self.connection.cursor()

    def _is_in_cache(self):
        count = self.cursor.execute('SELECT count(*) c FROM searches WHERE URL = ? AND date = ? AND tier = ? AND page = ?;',
            (self.apiUrl, self.date.isoformat(), self.tier, self.page)).fetchall()[0][0]
        return count == 1

    def _load_from_cache(self):
        return self.cursor.execute('SELECT result FROM searches WHERE URL = ? AND date = ? AND tier = ? AND page = ?;', (self.apiUrl, self.date.isoformat(), self.tier, self.page)).fetchall()[0][0]

    def __iter__(self):
        self.buffer = []
        self.page = 0
        self.tier = 0
        return self

    def __next__(self):
        if self.buffer == []:
        #   print(self.page, self.only_first_tier, self.tier)
            if (self.page == 0 and self.tier == 1 and self.only_first_tier) or (self.tier == -1):
                raise StopIteration

            print('Downloading page %d, tier %d from 3Taps' % (self.page, self.tier))
            if self._is_in_cache():
                text = self._load_from_cache()
            else:
                response = requests.get(self.apiUrl, params = {'tier':self.tier,'page':self.page}, proxies = proxies, auth = auth)
                text = response.text
                sql = '''
                INSERT INTO searches
                ("url","date","tier","page","result")
                VALUES (?,?,?,?,?)
                '''
                self.cursor.execute(sql, (self.apiUrl, self.date.isoformat(), self.tier, self.page, text))
                self.connection.commit()

            data = json.loads(text)

            if 'postings' not in data:
                raise StopIteration

            self.buffer = [p['external_url'] for p in data['postings']]
            self.page = data['next_page']
            self.tier = data['next_tier']
            print('The search returned %d results.' % data['num_matches'])

        return self.buffer.pop(0)

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
        return datetime.datetime.astimezone(e).isoformat()

if __name__ == '__main__':
    main()
