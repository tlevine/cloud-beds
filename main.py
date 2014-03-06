from craigsgenerator import craigsgenerator
import requests

from cloud_beds.db import db

from config import proxies, database, cachedir

def main():
    cg = craigsgenerator(get = get, threads_per_section = 10, superthreaded = False,
                         sites = ['chicago.craigslist.org'], sections = ['sub'],
                         cachedir = cachedir)

    sink = db(database)
    next(sink)

    for listing in cg:
        sink.send(listing)

def get(url):
    return requests.get(url, proxies = proxies)

if __name__ == '__main__':
    main()
