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
    for listing in Section(subdomain, 'sub'):
        print(listing)
        break

def furnished(text):
    return 'furnished' in text and not 'unfurnished' in text

def weekly(html):
    return 'week' in html.text_content()

if __name__ == '__main__':
    main()
