#!/usr/bin/env python3
import os
import csv
import threading
from queue import Queue

from craigsgenerator import Section, fulltext

from dates import is_date_range, dates, month

try:
    from config import http_proxy, http_proxy_username, http_proxy_username, http_proxy_password
    proxies = {'http':'http://%s:%s@%s' % (http_proxy_username, http_proxy_password, http_proxy)}
except ImportError:
    proxies = None


def sink(queue, fn = '/tmp/sublets.csv'):
    fieldnames = [
        'subdomain',
        'title', 'date', 'price',
        'longitude', 'latitude',
        'url', 'body',
    ]
    with open(fn, 'w') as fp:
        w = csv.DictWriter(fp, fieldnames)
        w.writeheader()
    while True:
        listing = queue.get()
        with open(fn, 'a') as fp:
            w = csv.DictWriter(fp, fieldnames)
            w.writerow(listing)

def main():
    queue = Queue()
    threading.Thread(target = sink, args = (queue,)).start()
    for subdomain in ['austin','newyork','sfbay','philadelphia','chicago','washingtondc','portland','seattle','boston']:
        for sectionslug in ['roo','sub','hsw','swp','vac','prk','off','rea']:
            t = threading.Thread(target = search_subdomain, args = (subdomain, sectionslug, queue))
            t.start()

def search_section(subdomain, sectionslug, queue):
    for listing in Section(subdomain, sectionslug, proxies = proxies, scheme = 'http'):
        # Make this parallel.
#       if os.path.getsize(listing['listing'].name) == 0:
#           os.remove(listing['listing'].name)
#           # Skip it; it'll get caught next time.
#           continue

        try:
            body = fulltext(listing)
        except KeyError:
            body = ''
        listing['body'] = body
        listing['url'] = listing['href']
        del(listing['href'])
        del(listing['listing'])
        queue.put(listing)

if __name__ == '__main__':
    main()
