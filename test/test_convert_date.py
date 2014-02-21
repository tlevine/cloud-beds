import nose.tools as n

from dates import convert_date

def check_convert_date(observed, expectation):
    result = convert_date(observed, year = 2014)
    if expectation == None:
        n.assert_equal(result, expectation)
    else:
        expected_month, expected_day = result
        n.assert_equal(result, datetime.date(2014, expected_month, expected_year))

testcases = [
    (['May', '1'], (5, 1)),
    (['July'], None),
    (None, None),
    (['April', '1st.'], (4, 1)),
    (['March'], None),
    (['may'], None),
]

def test_convert_date():
    for observed, expected in testcases:
        yield check_convert_date, observed, expected
