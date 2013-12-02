#!/usr/bin/env python3
import os
import lxml.html

from index import is_date_range

def check_is_date_range(filename):
    html = lxml.html.parse(os.path.join('fixtures',filename)).getroot()
    postingbody = html.xpath('id("postingbody")')[0].text_content()
    assert is_date_range(postingbody)

def test_is_date_range():
    for filename in filter(lambda x: x.endswith('.html'), os.listdir('fixtures')):
        yield check_is_date_range, filename
