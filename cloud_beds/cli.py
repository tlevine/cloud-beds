import warnings

from craigsgenerator import craigsgenerator
import requests

from cloud_beds.db import db, get_session

def main():
    if 'https_proxy' in os.environ:
        proxies = {'https': os.environ['https_proxy']}
    else:
        warnings.warn('I\'m not using a proxy because no https_proxy is set')
        proxies = {}
    database = 'postgres://localhost/craigslist'
    cachedir = os.path.join(os.environ['HOME'], 'dadawarehouse', 'cloud-sleeping')
    sections = ['sub']
    sites = ['philadelphia.craigslist.org']

    cg = craigsgenerator(get = get, threads_per_section = 10, superthreaded = False,
                         sites = sites, sections = sections,
                         cachedir = cachedir)

    sink = db(get_session(database))
    next(sink)

    for listing in cg:
        sink.send(listing)

def get(url):
    return requests.get(url, proxies = proxies)
