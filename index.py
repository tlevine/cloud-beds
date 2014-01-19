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
from is_date_range import is_date_range

import sqlite3

import requests
import parsedatetime.parsedatetime as pdt
cal = pdt.Calendar()
import lxml.html

def main():
    if not os.environ['APIKEY']:
        print('You need to set the APIKEY environment variable to your 3Taps API key.')
        exit(1)

    if not os.environ['REGION']:
        print('You need to set the REGION variable to the 3Taps region to search.')
        exit(1)

    s = search3Taps(os.environ['APIKEY'], os.environ['REGION'])
    outputfile = '/tmp/short-term-sublets.tsv'
    h = open(outputfile, 'w')
    h.write('price\turl\n')
    h.close()
    print('Writing short-term sublets to %s' % outputfile)
    for page in s:
    #   print(page)
        html = lxml.html.fromstring(loadCraigslist(page))
        if is_date_range(html):
            print('Has a date range:',page)
            h = open(outputfile, 'a')
            h.write('%d\t%s\n' % (price(html.text_content()),page))
            h.close()

def randomsleep(mean = 8, sd = 4):
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

        response = requests.get(requestUrl, headers = headers)
        open(fileName, 'w').write(response.text)
        randomsleep()
    return open(fileName).read()

class search3Taps:
    def __init__(self, apikey, region, rpp = 100, only_first_tier = False, min_price = 200, max_price = 1500):
        self.only_first_tier = only_first_tier
        args = {
            'apikey':apikey,
            'rpp':rpp,
            'min_price':min_price,
            'max_price':max_price,
            'region':region,
            'body':'~bnb.com',
        }
        self.apiUrl = "http://search.3taps.com?auth_token=%(apikey)s&SOURCE=CRAIG&location.region=%(region)s&category=RSUB&retvals=external_url&rpp=%(rpp)d&price=%(min_price)s..%(max_price)d&body=%(body)s" % args
        self.date = datetime.date.today()
        print(self.apiUrl)

        self.connection = sqlite3.connect('3taps.sqlite')
        self.cursor = self.connection.cursor()
        self.cursor.execute(open('schema.sql').read())
        self.connection.commit()

    def _is_in_cache(self):
        count = self.cursor.execute('SELECT count(*) c FROM searches WHERE URL = ? AND date = ?;', (self.apiUrl, self.date.isoformat())).fetchall()[0][0]
        return count == 1

    def _load_from_cache(self):
        return self.cursor.execute('SELECT result FROM searches WHERE URL = ? AND date = ?;', (self.apiUrl, self.date.isoformat())).fetchall()[0][0]

    def __iter__(self):
        self.buffer = []
        self.page = 0
        self.tier = 0
        return self

    def __next__(self):
        if self.buffer == []:
            print(self.page, self.only_first_tier, self.tier)
            if (self.page == 0 and self.tier == 1 and self.only_first_tier) or (self.tier == -1):
                raise StopIteration
            else:
                print('Downloading page %d, tier %d from 3Taps' % (self.page, self.tier))
                if self._is_in_cache():
                    text = self._load_from_cache()
                else:
                    response = requests.get(self.apiUrl, params = {'tier':self.tier,'page':self.page})
                    text = response.text
                    sql = '''
                    INSERT INTO searches
                    ("url","date","tier","page","result")
                    VALUES (?,?,?,?,?)
                    '''
                    self.cursor.execute(sql, (self.apiUrl, self.date.isoformat(), self.tier, self.page, text))
                    self.connection.commit()

                data = json.loads(text)
                self.buffer = [p['external_url'] for p in data['postings']]
                self.page = data['next_page']
                self.tier = data['next_tier']
                print('The search returned %d results.' % data['num_matches'])

        return self.buffer.pop(0)

def price(text):
    'Find the price of a listing. Use the highest dollar value in the listing.'
    numbers = re.findall(r'[$0-9]+', re.sub(r'[, ]', '', text))
    monies = filter(lambda x: '$' in x, numbers)
    integers = map(int, (money.replace('$','') for money in monies))
    return max(integers)

if __name__ == '__main__':
    main()
