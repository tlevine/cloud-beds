from index import price
import nose.tools

cases = [
    ('$300',300),
    ('$1,232',1232),
    ('340$',340),
    ('oeu $ 382 oeuoeu',382),
    ('o823423eu $ 382 oeu $83 oeu',382),
]

def check_price(raw, expected):
    nose.tools.assert_equal(price(raw), expected)

def test_price():
    for raw, expected in cases:
        yield check_price, raw, expected
