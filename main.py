#!/usr/bin/env python3
import threading

from craigsgenerator import Section, fulltext

from dates import is_date_range, dates, month

try:
    from config import http_proxy, http_proxy_username, http_proxy_username, http_proxy_password
    proxies = {'http':'http://%s:%s@%s' % (http_proxy_username, http_proxy_password, http_proxy)}
except ImportError:
    proxies = None


def Sink():
    while True:
        listing = yield
        print(listing)

def main():
    sink = Sink()
    sink.send(None)
    for subdomain in ['austin','newyork','sfbay','philadelphia','chicago','washingtondc']:
        t = threading.Thread(target = search_subdomain, args = (subdomain, sink))
        t.start()

def search_subdomain(subdomain, sink):
    for listing in Section(subdomain, 'sub', proxies = proxies, scheme = 'http'):
        listing['listing'] = fulltext(listing)
        sink.send(listing)

if __name__ == '__main__':
    main()
