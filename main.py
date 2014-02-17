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
    for subdomain in ['austin','newyork','sfbay','philadelphia','chicago','washingtondc']:
        t = threading.Thread(target = search_subdomain, args = (subdomain, queue))
        t.start()

def search_subdomain(subdomain, queue):
    for listing in Section(subdomain, 'sub', proxies = proxies, scheme = 'http'):
#       if os.path.getsize(listing['listing'].name) == 0:
#           os.remove(listing['listing'].name)
#           # Skip it; it'll get caught next time.
#           continue

        # Make this parallel.
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
