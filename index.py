#!/usr/bin/env python3
import os
from urllib.parse import urlparse
import re
import json
import itertools
from time import sleep
from random import normalvariate

import requests
import parsedatetime.parsedatetime as pdt
cal = pdt.Calendar()
import lxml.html

def main():
    if not os.environ['APIKEY']:
        print('You need to set the APIKEY environment variable to your 3Taps API key.')
        exit(1)
    else:
        s = search3Taps(os.environ['APIKEY'])
        for page in s:
        #   print(page)
            html = lxml.html.fromstring(loadCraigslist(page))
            postingbody = html.xpath('id("postingbody")')[0].text_content()
            if is_date_range(postingbody):
                print('Has a date range:',page)

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
    def __init__(self, apikey, rpp = 100, only_first_tier = True, max_price = 1500):
        self.only_first_tier = only_first_tier

        args = {'rpp':rpp,'max_price':max_price,'apikey':apikey,
            'region':'|'.join(map(lambda x:'USA-NYM-'+x, ['BRN','BRO','LON','MAN','QUE']))}
        self.apiUrl = "http://search.3taps.com?auth_token=%(apikey)s&SOURCE=CRAIG&location.region=%(region)s&category=RSUB&retvals=external_url&rpp=%(rpp)d&price=..%(max_price)d" % args
        print(self.apiUrl)

    def __iter__(self):
        self.buffer = []
        self.page = 0
        self.tier = 0
        return self

    def __next__(self):
        if self.buffer == []:
            if (self.page == -1 and self.only_first_tier) or (self.tier == -1):
                raise StopIteration
            else:
                print('Downloading page %d, tier %d from 3Taps' % (self.page, self.tier))
                response = requests.get(self.apiUrl, params = {'tier':self.tier,'page':self.page})
                data = json.loads(response.text)
                self.buffer = [p['external_url'] for p in data['postings']]
                self.page = data['next_page']
                self.tier = data['next_tier']

        return self.buffer.pop(0)

def is_date_range(postingbody):
    body = iter(postingbody.split(' '))
    for _ in body:
        bag = tuple(itertools.islice(body, 7))
        was_date = False
        n_dates = 0
        for token in bag:
            if (not was_date) and  is_date(token):
                n_dates += 1
            was_date = is_date(token)
        if n_dates >= 2:
        #   print(bag)
        #   print(tuple(map(is_date, bag)))
            return True
    return False

def is_date(s):
    parsedatetime_can_parse = cal.parse(s)[1] == 1
    if parsedatetime_can_parse:
        return True
    return False

if __name__ == '__main__':
    main()
