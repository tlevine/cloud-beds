import is_date_range
import nose.tools as n

def check_is_date(tokens, expectation):
    n.assert_equal(is_date_range.is_date(tokens), expectation)

def check_token_is_month(token, expectation):
    n.assert_equal(is_date_range._token_is_month(token), expectation)

def check_token_is_day_of_month(token, expectation):
    n.assert_equal(is_date_range._token_is_day_of_month(token), expectation)

def check_n_dates(string, expectation):
    the_list = list(is_date_range.dates_in_tokens(string.split(' ')))
    print(the_list)
    n.assert_equal(len(the_list), expectation)

daterange_testcases = [
    ('January 6 - January 31',2),
    ('January 6 - January',2),
    ('January 6',1),
    ('January',1),
    ('January 31 (Rego',1),
    ('1br - December to January Sublet in bedstuy',2),
    ('1br',0),
    ('December to January',2),
    ('January Sublet',1),
    ('December to',1),
    ('December',1),
    ('December 19th to January',2),
    ('19th to',0),
    ('December 19th',1),
    ('January 18th',1),
    ('December 19th.',1),
    ('January 18th.',1),
    ('January 5th. $2200',1),
    ('from December',1),
]

date_testcases_lists = [
    ([], False),
    ([''], False),
]

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
    ('December',True),
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

def test_dates_in_tokens():
    for string, expectation in daterange_testcases:
        yield check_n_dates, string, expectation

def test_is_ordinal_number():
    n.assert_false(is_date_range._is_ordinal_number('24st'))

def test_is_date():
    for string, expectation in date_testcases:
        yield check_is_date, string.split(' '), expectation

    for tokens, expectation in date_testcases_lists:
        yield check_is_date, tokens, expectation

def test_token_is_month():
    for token, expectation in month_testcases:
        yield check_token_is_month, token, expectation

def test_token_is_day_ofmonth():
    for token, expectation in day_of_month_testcases:
        yield check_token_is_day_of_month, token, expectation
