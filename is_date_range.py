'Train this on the fixtures.'
import warnings
import os
import re
import itertools

import lxml.html
import pandas

def main():
    df = pandas.read_csv(os.path.join('fixtures','fixtures.csv')).head()
    df.index = df['url'].map(lambda url: int(url.split('/')[-1].split('.')[0]))
    df['filename'] = df['url'].map(lambda url: os.path.join('fixtures',url.split('/')[-1]))
    df['html'] = df['filename'].map(lambda x: lxml.html.parse(x).getroot())

def is_date_range(html):
    postingbodies = html.xpath('id("postingbody")')
    if len(postingbodies) > 0:
        postingbody = postingbodies[0].text_content()
    else:
        warnings.warn('No #postingbody found on the page')
        return False

    titles = html.xpath('//title')
    if len(titles) > 0:
        title = titles[0].text_content()
    else:
        warnings.warn('No <title /> found on the page')
        return False


    for text in [title, postingbody]:
        if 'for the month' in text:
            return True

        body = iter(text.split(' '))
        for window in _ngrams(body):
#           print(window)
            if len(list(dates_in_tokens(window))) == 2:
                return True
            else:
                for i in range(1, len(window)):
                    if _is_end_date(window[0], window[1:i]):
                        print(window[0], window[1:i])
                        return True
    return False

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
            _token_is_immediate,
        ]:
            if func(token):
                return True

    if tokens == []:
        return False

    for i in range(1, len(tokens) + 1):
        window = tokens[:i]
        if set(map(_token_is_date,window)) == {True}:
            pass
        elif _token_is_date(window[0]) and set(map(_token_is_day_of_month,window[1:])) == {True}:
            pass
        else:
            return False

    return True

def _is_end_date(prevword, window):
    return prevword in {
        'til','till','through','until',
        '--','-',
        'ends', 'ending',
    } and is_date(window)

def _token_is_immediate(token):
    return token.lower() in {
        'now',
        'today',
    }

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

def _ngrams(tokens, n = 7):
    l = list(tokens)
    return (l[i:i+n] for i in range(len(l)-n))
