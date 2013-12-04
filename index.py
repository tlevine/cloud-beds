#!/usr/bin/env python3
import warnings
import os
from urllib.parse import urlparse
import re
import json
import itertools
from time import sleep
from random import normalvariate
from is_date_range import is_date_range

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
    def __init__(self, apikey, rpp = 100, only_first_tier = True, max_price = 1500):
        self.only_first_tier = only_first_tier

        nyc_regions = list(map(lambda x:'USA-NYM-'+x, ['BRO','MAN','QUE']))
        regions = nyc_regions + ['USA-WAS-DIS']
        args = {'rpp':rpp,'max_price':max_price,'apikey':apikey,
            'region':'|'.join(regions),
            'body':'~bnb.com',
        }
        self.apiUrl = "http://search.3taps.com?auth_token=%(apikey)s&SOURCE=CRAIG&location.region=%(region)s&category=RSUB&retvals=external_url&rpp=%(rpp)d&price=200..%(max_price)d&body=%(body)s" % args
        print(self.apiUrl)

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
                try:
                    os.mkdir('3taps')
                except OSError:
                    pass

                filename_3taps = os.path.join('3taps','tier%d-page%d' % (self.tier, self.page))
                if os.path.exists(filename_3taps):
                    data = json.load(open(filename_3taps))
                else:
                    response = requests.get(self.apiUrl, params = {'tier':self.tier,'page':self.page})
                    open(filename_3taps, 'w').write(response.text)
                    data = json.loads(response.text)
                self.buffer = [p['external_url'] for p in data['postings']]
                self.page = data['next_page']
                self.tier = data['next_tier']
                print('The search returned %d results.' % data['num_matches'])

        return self.buffer.pop(0)

def price(text):
    'Find the price of a listing. Use the highest dollar value in the listing.'
    monies = re.findall(r'[$0-9]+', re.sub(r'[, ]', '', text))
    numbers = map(int, (money.replace('$','') for money in monies))
    return max(numbers)

if __name__ == '__main__':
    main()
