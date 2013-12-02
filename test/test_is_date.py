import is_date_range
import nose.tools as n

def check_is_date(string, expectation):
    n.assert_equal(is_date_range.is_date(string.split(' ')), expectation)

def check_token_is_month(token, expectation):
    n.assert_equal(is_date_range._token_is_month(token), expectation)

def check_token_is_day_of_month(token, expectation):
    n.assert_equal(is_date_range._token_is_day_of_month(token), expectation)

def test_is_ordinal_number():
    n.assert_false(is_date_range._is_ordinal_number('24st'))

date_testcases = [
    ('January 6 - January 31',False),
    ('January 6 - January',False),
    ('January 6',True),
    ('January',True),
    ('January 31 (Rego',False),
    ('1br - December to January Sublet in bedstuy',False),
    ('1br',False),
    ('December to January',False),
    ('January Sublet',False),
    ('December to',False),
    ('December',True),
    ('December 19th to January',False),
    ('19th to',False),
    ('December 19th',True),
    ('January 18th',True),
    ('December 19th.',True),
    ('January 18th.',True),
    ('January 5th. $2200',False),
    ('from December',False),
]

month_testcases = [
    ('6',False),
    ('January',True),
    ('january',True),
    ('jan',True),
    ('(Rego',False),
    ('1br',False),
]

day_of_month_testcases = [
    ('6',True),
    ('1br',False),
    ('1st',True),
    ('2br',False),
    ('2nd',True),
    ('3br',False),
    ('3rd',True),
    ('4br',False),
    ('4th',True),
    ('24th',True),
    ('24st',False),
    ('24th.',True),
    ('$30',False),
]

@n.nottest
def test_is_date():
    for string, expectation in date_testcases:
        yield check_is_date, string, expectation

@n.nottest
def test_token_is_month():
    for token, expectation in month_testcases:
        yield check_token_is_month, token, expectation

def test_token_is_day_ofmonth():
    for token, expectation in day_of_month_testcases:
        yield check_token_is_day_of_month, token, expectation
