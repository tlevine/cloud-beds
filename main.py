#!/usr/bin/env python3
import os
import csv
import threading
from queue import Queue
import itertools

from craigsgenerator import Section, fulltext

from dates import is_date_range, dates, month

proxy_schemes = {'http_proxy','https_proxy'}
if len(proxy_schemes.intersection(os.environ.keys())) > 0:
    proxies = {s.replace('_proxy',''):os.environ[s] for s in proxy_schemes if s in os.environ}
else:
    try:
        from config import proxies
    except ImportError:
        proxies = None

SUBDOMAINS = ['austin','newyork','sfbay','philadelphia','chicago','washingtondc','portland','seattle','boston']
SECTIONS = ['roo','sub','hsw','swp','vac','prk','off','rea']

def save(queue, fn = '/tmp/sublets.csv'):
    if os.path.exists(fn):
        with open(fn, 'r') as fp:
            r = csv.DictReader(fp)
            skip = set((row['url'] for row in r))
    else:
        skip = set()

    fieldnames = [
        'subdomain','section',
        'title', 'date', 'price',
        'longitude', 'latitude',
        'url', 'body',
    ]
    with open(fn, 'w') as fp:
        w = csv.DictWriter(fp, fieldnames)
        w.writeheader()

    for i in itertools.count(1):
        listing = queue.get()
        with open(fn, 'a') as fp:
            w = csv.DictWriter(fp, fieldnames)
            w.writerow(listing)

        if i % 100 == 0:
            print('Written %d records' % i, end = '\r')

def count(queue):
    for i in itertools.count(1):
        queue.get()
        if i % 100 == 0:
            print('Written %d records' % i, end = '\r')

def log(queue):
    for i in itertools.count(1):
        print('% 10d: %s' % (i,queue.get()['href']))

def download(targetfunc, queuefunc, subdomains = SUBDOMAINS, sections = SECTIONS):
    queue = Queue()
    threading.Thread(target = queuefunc, args = (queue,)).start()
    for subdomain in subdomains:
        for section in sections:
            t = threading.Thread(target = targetfunc, args = (subdomain, section, queue))
            t.start()

def download_section(subdomain, sectionslug, queue):
    for listing in Section(subdomain, sectionslug, proxies = proxies, scheme = 'https'):
        queue.put(listing)

def read_section(subdomain, sectionslug, queue):
    for listing in Section(subdomain, sectionslug, proxies = proxies, scheme = 'https'):
        # Make this parallel?
        try:
            body = fulltext(listing)
        except KeyError:
            body = ''
        listing['body'] = body

        listing['subdomain'] = subdomain
        listing['section'] = sectionslug
        listing['url'] = listing['href']

        del(listing['href'])
        del(listing['listing'])
        queue.put(listing)

if __name__ == '__main__':
    download(read_section, save)
    # download(download_section, count)
    # download(download_section, log)
    # download(read_section, save, subdomains = ['austin'], sections = ['sub'])
