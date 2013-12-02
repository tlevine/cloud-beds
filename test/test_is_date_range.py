#!/usr/bin/env python3
import os
import csv

import lxml.html
import nose.tools as n

from index import is_date_range

def check_is_date_range(filename, expected):
    html = lxml.html.parse(filename).getroot()
    postingbody = html.xpath('id("postingbody")')[0].text_content()
    n.assert_equal(is_date_range(postingbody), expected)

def test_is_date_range():
    r = csv.DictReader(open(os.path.join('fixtures','fixtures.csv')))
    for row in r:
        filename = os.path.join('fixtures', row['url'].split('/')[-1])
        if os.path.isfile(filename):
            expected = row['has.date.range'] == 'TRUE'
            yield check_is_date_range, filename, expected
