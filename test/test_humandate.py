import lxml.html
import datetime
import nose.tools as n

from dates import humandate

html = lxml.html.parse('fixtures/4220326964.html').getroot()

def test_posted():
    observed = humandate('Posted: ', html)
    expected = int(datetime.datetime(2013, 11, 30, 2, 0, 46).timestamp())
    n.assert_equal(observed, expected)

def test_updated():
    observed = humandate('Updated: ', html)
    expected = int(datetime.datetime(2013, 12, 2, 2, 31, 59).timestamp())
    n.assert_equal(observed, expected)
