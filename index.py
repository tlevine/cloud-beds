#!/usr/bin/env python3
import os
from urllib.parse import urlparse
import re
import json

import requests

def main():
    if not os.environ['APIKEY']:
        print('You need to set the APIKEY environment variable to your 3Taps API key.')
        exit(1)
    else:
        body = search3Taps(2, APIKEY)


def loadCraigslist(craigslistUrl):
    httpCraigslistUrl = 'http://' + craigslistUrl.replace(r'^https?://','')
    parsedUrl = urlparse(craigslistUrl)
    requestUrl = 'http://' + re.sub(r'http://', '', httpCraigslistUrl)
    fileName = 'craigslist/' + parsedUrl.hostname.replace(r'\..*$', '') + parsedUrl.path;

    if not os.path.exists(fileName):
        try:
            os.makedirs(re.sub(r'\/[^\/]*$', '', fileName))
        except OSError:
            pass

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0"
        }

        response = requests.get(requestUrl, headers = headers)
        open(fileName, 'w').write(response.text)
    return open(fileName).read()

def search3Taps(rpp, apikey):
    apiUrl = "http://search.3taps.com?auth_token=" +  apikey + \
        "&SOURCE=CRAIG&location.state=USA-NY&category=RSUB&retvals=external_url&rpp=" + str(rpp);

    response = requests.get(apiUrl)
    return json.loads(response.text)

if __name__ == '__main__':
#   print(loadCraigslist('http://newyork.craigslist.org/mnh/sub/4199556907.html'))
    print(search3Taps(2, os.environ['APIKEY']))
    #main()
