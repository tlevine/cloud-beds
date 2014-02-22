from nose.tools import assert_list_equal
from dates import tokenize

testcases = [
    ('January 6 - January 31', ['January', '6', '-', 'January', '31']),
    ('January 6 - January', ['January', '6', '-', 'January']),
    ('January 6', ['January', '6']),
    ('January', ['January']),
    ('January 31 (Rego', ['January', '31', '(Rego']),
    ('1br - December to January Sublet in bedstuy',['1br', 'December', 'to', 'January', 'Sublet', 'in', 'bedstuy']),
    ('1br',['1br']),
    ('December to January',['December', 'to', 'January']),
    ('January Sublet',['January', 'Sublet']),
    ('December to',['December', 'to']),
    ('December',['December']),
    ('December 19th to January',['December', '19th', 'to', 'January']),
    ('19th to',['19th', 'to']),
    ('December 19th',['December', '19th']),
    ('January 18th',['January', '18th']),
    ('December 19th.',['December', '19th.']),
    ('January 18th.',['January', '18th.']),
    ('January 5th. $2200',['January', '5th.', '$2200']),
    ('from December',['from', 'December']),
    ('Dec 15 - Feb 1.',['Dec 15', 'Feb 1.']),
    ('Pool Area\nAvailable for March 1-May 31, 2014 (ask for details)\n\nWil', ['Pool', 'Area', 'Available', 'for', 'March', '1', 'May', '31,', '2014', '(ask', 'for details)', 'nWil']),
    ('March 1-May 31, 2014', ['March', '1', 'May', '31,', '2014']),
]

def check_tokenize(raw, expected):
    assert_list_equal(tokenize(raw), expected)

def test_tokenize():
    for raw, expected in testcases:
        yield check_tokenize, raw, expected
