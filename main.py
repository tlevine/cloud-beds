import os

from craigsgenerator import craigsgenerator

from cloud_beds.db import db

from config import proxies, database

def main():
    cg = craigsgenerator(get = get, threads_per_section = 10, superthreaded = False,
                         sites = ['chicago.craigslist.org'],
                         cachedir = os.path.join(os.environ['HOME'], 'dadawarehouse', 'craigslist'))

    sink = db(database)
    next(sink)

    for listing in cg:
        save(listing)

def get(url):
    return requests.get(url, proxies = proxies)

if __name__ == '__main__':
    main()
