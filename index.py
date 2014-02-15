#!/usr/bin/env python3
import datetime
import warnings
import os
import sys
from urllib.parse import urlparse
import re
import json
import itertools
from time import sleep
from random import normalvariate
from is_date_range import is_date_range, dates, month
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
    from config import http_proxy, http_proxy_username, http_proxy_username, http_proxy_password
    proxies = {'http':'http://' + http_proxy}
    auth = requests.auth.HTTPProxyAuth(http_proxy_username, http_proxy_password)
except ImportError:
    proxies = None

def main():
    for subdomain in ['austin']:
        t = threading.Thread(target = search_subdomain, args = (subdomain,))
        t.start()

def search_subdomain(subdomain):
    s = Search(subdomain)
    for url in s:
        get(url)
        break

class Search:
    def __init__(self, subdomain):
        self.subdomain = subdomain

    def __iter__(self):
        self.buffer = []
        self.html = None
        self.present_search_url = None
        return self

    def __next__(self):
        if self.buffer == []:
            self.download()
            self.buffer.extend(map(str,self.html.xpath('//p[@class="row"]/a/@href')))

        if self.html.xpath('count(//p[@class="row"])') == 0:
            logger.debug('Stopped at %s' % self.present_search_url)
            raise StopIteration
        else:
            return self.buffer.pop(0)

    def download(self):
        self.present_search_url = self.next_search_url()
        fp = get(self.present_search_url)

        html = lxml.html.fromstring(fp.read())
        html.make_links_absolute(self.present_search_url)
        self.html = html

    def next_search_url(self):
        'Determine the url of the next search page.'
        if not self.html:
            return 'https://%s.craigslist.org/sub/index000.html' % self.subdomain

        nexts = set(self.html.xpath('//a[contains(text(),"next >")]/@href'))
        if len(nexts) != 1:
            raise ValueError('No next page for %s' % self.search_url)
        return str(list(nexts)[0])


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

def weekly(html):
    return 'week' in html.text_content()

#if __name__ == '__main__':
#    main()
