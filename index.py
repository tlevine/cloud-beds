#!/usr/bin/env python3
import threading

from craigsgenerator import Section, fulltext
from dates import is_date_range, dates, month

try:
    from config import http_proxy, http_proxy_username, http_proxy_username, http_proxy_password
    proxies = {'http':'http://%s:%s@' % (http_proxy_username, http_proxy_password, http_proxy)}
except ImportError:
    proxies = None

def main():
    for subdomain in ['austin']:
        t = threading.Thread(target = search_subdomain, args = (subdomain,))
        t.start()

def search_subdomain(subdomain):
    for listing in Section(subdomain, 'sub'):
        print(listing)
        break

if __name__ == '__main__':
    main()
