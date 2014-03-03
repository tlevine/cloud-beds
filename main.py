from craigsgenerator import craigsgenerator

from config import proxies

from cloud_beds.db import db

def main():
    cg = craigsgenerator(get = get, threads_per_section = 10, superthreaded = False,
        cachedir = os.path.join(os.environ['HOME'], 'dadawarehouse', 'craigslist'))

    sink = db()
    next(sink)

    for listing in cg:
        save(listing)

def get(url):
    return requests.get(url, proxies = proxies)
