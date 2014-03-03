from craigsgenerator.generators import sites, listings
from craigsgenerator import craigsgenerator

from config import proxies

def get(url):
    return requests.get(url, proxies = proxies)

def craigsgenerator(sites = lambda: sites(get = get), listings = lambda: listings(get = get),
                    sections = ['sub'], threaded = True):
