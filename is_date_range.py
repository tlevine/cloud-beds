'Train this on the fixtures.'
import os
import re

import lxml.html
import pandas

def main():
    df = pandas.read_csv(os.path.join('fixtures','fixtures.csv')).head()
    df.index = df['url'].map(lambda url: int(url.split('/')[-1].split('.')[0]))
    df['filename'] = df['url'].map(lambda url: os.path.join('fixtures',url.split('/')[-1]))
    df['html'] = df['filename'].map(lambda x: lxml.html.parse(x).getroot())

def dates_in_tokens(tokens):
    current_date = []
    for token in tokens:
        if is_date(current_date + [token]):
            current_date.append(token)
        elif is_date(current_date):
            yield current_date
            current_date = []
        elif current_date == []:
            pass
        else:
            assert False
    if current_date != []:
        yield current_date

def is_date(tokens: list) -> bool:
    '''
    Given a list of words, determine whether the list
    collectively forms a single date.

    >>> is_date('From January')
    False

    >>> is_date('January')
    True

    >>> is_date('January 3')
    True

    >>> is_date('January 3 to')
    False

    '''
    def _token_is_date(token):
        for func in [
            _token_is_datestamp,
            _token_is_month,
            _token_is_day_of_month,
            _token_is_year,
        ]:
            if func(token):
                return True
        return False
    return set(map(_token_is_date,tokens)) == {True}

def _token_is_month(token):
    months = {
        'january','february','march','april',
        'may','june','july','august',
        'september','october','november','december',
    }
    months=months.union([month[:3] for month in months])
    return token.lower() in months

def _token_is_datestamp(token):
    return False

def _is_ordinal_number(num):
    digits = re.sub(r'[^0-9]','',num)
    letters = re.sub(r'[^a-z]','',num.lower())
    if digits == '':
        return False
    suffixes = ["th", "st", "nd", "rd", ] + ["th"] * 16 +  ["th", "st", "nd", "rd", ] + ["th"] * 7 + ["st"]
    return letters == suffixes[int(digits) % 100]

def _token_is_day_of_month(token):
    digits = re.sub(r'[^0-9]','',token)
    if digits == '':
        for word in ['first','last','end']:
            if word in token.lower():
                return True
        return False
    else:
        for forbidden in ['$','br','ave']:
            if forbidden in token.lower():
                return False

        potential_day = int(digits)
        if not 1 <= potential_day <= 31:
            return False

        if len(token) >= 3:
            return _is_ordinal_number(token)
        else:
            return True

def _token_is_year(token):
    return False
