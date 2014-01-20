import lxml.html
import datetime
import nose.tools as n

from index import craigsdate

html = lxml.html.parse('fixtures/4220326964.html').getroot()

def test_posted():
    observed = craigsdate('Posted: ', html)
    expected = int(datetime.datetime(2013, 11, 30, 2, 0, 46).timestamp())
    n.assert_equal(observed, expected)

def test_updated():
    observed = craigsdate('Updated: ', html)
    expected = int(datetime.datetime(2013, 12, 2, 2, 31, 59).timestamp())
    n.assert_equal(observed, expected)
