import datetime

import nose.tools as n

from dates import convert_date, convert_dates

def check_convert_date(raw, expectation):
    result = convert_date(raw, year = 2014)
    if expectation == None:
        n.assert_is_none(result)
    else:
        expected_month, expected_day = expectation
        n.assert_equal(result, datetime.date(2014, expected_month, expected_day))

def test_convert_date():
    testcases = [
        (['May', '1'], (5, 1)),
        (['July'], None),
        (None, None),
        (['April', '1st.'], (4, 1)),
        (['March'], None),
        (['may'], None),
    ]
    for raw, expected in testcases:
        yield check_convert_date, raw, expected

def check_convert_dates(raw, expectation):
    result = convert_dates(raw, lambda x: convert_date(x, year = 2014))
    if expectation == None:
        n.assert_is_none(result)
    else:
        n.assert_is_not_none(result)
        observed = tuple((x.month, x.day) for x in sorted(result))
        n.assert_tuple_equal(observed, expected)

def test_convert_dates():
    testcases = [
        ((['May', '1'], ['July']), None),
        ((['May', '1'], ['April', '1st.']), ((4,1),(5,1))),
        ((['Jan', '4'], ['April', '3rd.']), ((1,4),(4,3))),
    ]
    for raw, expected in testcases:
        yield check_convert_dates, raw, expected
