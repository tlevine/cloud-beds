import nose.tools as n

from months import start_end

testcases = [
    ('march 3 to april 3', (3,4)),
    ('January 19th-May 31st', (1,5)),
    ('January 19th', (1,1)),
    ('sudoroom', None),
]

def check_months(raw, expected):
    observed = start_end(raw)
    if expected == None:
        n.assert_is_none(observed)
    else:
        n.assert_tuple_equal(observed, expected)

def test_months():
    for raw, expected in testcases:
        yield check_months, raw, expected
