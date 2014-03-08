import warnings
import os

from craigsgenerator import craigsgenerator
import requests

from cloud_beds.db import db, get_session

def get_generator():
    if 'https_proxy' in os.environ:
        proxies = {'https': os.environ['https_proxy']}
    else:
        warnings.warn('I\'m not using a proxy because no https_proxy is set')
        proxies = {}

    def get(url):
        return requests.get(url, proxies = proxies)

    cachedir = os.path.join(os.environ['HOME'], 'dadawarehouse.thomaslevine.com', 'cloud-beds')
    sections = ['sub']
    sites = ['philadelphia.craigslist.org']

    return craigsgenerator(get = get, threads_per_section = 10, superthreaded = False,
                           sites = sites, sections = sections,
                           cachedir = cachedir)

def main():
    database = os.environ['CLOUD_BEDS_DB']
    cg = get_generator()
    sink = db(get_session(database))
    for listing in cg:
        sink.send(listing)
