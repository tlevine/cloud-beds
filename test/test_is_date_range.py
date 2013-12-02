#!/usr/bin/env python3
import os
import lxml.html

from index import is_date_range

def check_is_date_range(html):
    assert is_date_range(html)

for filename in filter(lambda x: x.endswith('.html'), os.listdir('fixtures')):
    html = lxml.html.parse(os.path.join('fixtures',filename)).getroot()
    yield check_is_date_range, html.text_content()
