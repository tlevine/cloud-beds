#!/usr/bin/env python3
import os
from urllib.parse import urlparse
import re
import json
import itertools
from time import sleep

import requests
import parsedatetime.parsedatetime as pdt
cal = pdt.Calendar()

def main():
    if not os.environ['APIKEY']:
        print('You need to set the APIKEY environment variable to your 3Taps API key.')
        exit(1)
    else:
        s = search3Taps(os.environ['APIKEY'])
        for page in s:
            print(page)
            sleep(1)


def loadCraigslist(craigslistUrl):
    httpCraigslistUrl = 'http://' + craigslistUrl.replace(r'^https?://','')
    parsedUrl = urlparse(craigslistUrl)
    requestUrl = 'http://' + re.sub(r'http://', '', httpCraigslistUrl)
    fileName = 'craigslist/' + parsedUrl.hostname.replace(r'\..*$', '') + parsedUrl.path;

    if not os.path.exists(fileName):
        try:
            os.makedirs(re.sub(r'\/[^\/]*$', '', fileName))
        except OSError:
            pass

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0"
        }

        response = requests.get(requestUrl, headers = headers)
        open(fileName, 'w').write(response.text)
    return open(fileName).read()

class search3Taps:
    def __init__(self, apikey, rpp = 100, only_first_tier = True):
        self.apiUrl = "http://search.3taps.com?auth_token=" + apikey + \
            "&SOURCE=CRAIG&location.metro=USA-NYM&category=RSUB&retvals=external_url&rpp=" + str(rpp)
        self.tier = 0
        self.page = 0
        self.buffer = []

    def __iter__(self):
        if self.buffer == []:
            response = requests.get(self.apiUrl, params = {'tier':self.tier,'page':self.page})
            self.data = json.loads(response.text)
            self.buffer = [p['external_url'] for p in self.data['postings']]
        return self

    def __next__(self):
        result = self.buffer.pop(0)
        if self.buffer == []:
            self.page = self.data['next_page']
            self.tier = self.data['next_tier']

            if (self.data['next_page'] == -1 and only_first_tier) or (self.data['next_tier'] == -1):
                raise StopIteration

            return self.data
        return result

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
