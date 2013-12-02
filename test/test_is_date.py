from is_date_range import is_date
import nose.tools as n

def check_is_date(string, expectation):
    n.assert_equal(is_date(string.split(' ')), expectation)

testcases = [
    ('January 6 - January 31',False)
    ('January 6 - January',False)
    ('January 6',True)
    ('January',True)
    ('January 31 (Rego',False)
    ('1br - December to January Sublet in bedstuy',False)
    ('1br',False)
    ('December to January',False)
    ('January Sublet',False)
    ('December to',False)
    ('December',True)
    ('December 19th to January',False)
    ('19th to',False)
    ('December 19th',True)
    ('January 18th',True)
    ('December 19th.',True)
    ('January 18th.',True)
    (,)
    (,)
    (,)
]

def test_is_date():
    for string, expectation in testcases:
        yield check_is_date, string, expectation
