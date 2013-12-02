from is_date_range import is_date
import nose.tools as n

def check_is_date(string, expectation):
    n.assert_equal(is_date(string), expectation)

testcases = [
    (,)
    (,)
    (,)
    (,)
    (,)
    (,)
]

def test_is_date():
    for string, expectation in testcases:
        yield check_is_date, string, expectation
