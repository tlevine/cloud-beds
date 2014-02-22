'Train this on the fixtures.'
import warnings
import os
import re
import itertools
import datetime
import csv
import dateutil

import lxml.html

def main():
    for row in csv.DictReader(os.path.join('fixtures','fixtures.csv')):
        index = row['url'].split('/')[-1].split('.')[0]
        filename = os.path.join('fixtures',row['url'].split('/')[-1])
        html = lxml.html.parse(filename).getroot()

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
#                       print(window[0], window[1:i])
                        return True
    return False

SHORT_MONTHS = [(i,datetime.date(2013, i, 1).strftime('%b')) for i in range(1, 13)]
LONG_MONTHS  = [(i,datetime.date(2013, i, 1).strftime('%B')) for i in range(1, 13)]
MONTHS = {m.lower():i for i,m in SHORT_MONTHS}
MONTHS.update({m.lower():i for i,m in LONG_MONTHS})

def month(dates_list):
    'From a date in my weird list date format to a datetime.date'
    if dates_list:
        for e in [d.lower() for d in dates_list]:
            if e in MONTHS:
                return MONTHS[e]
    return None

def dates(html):
    'Return my weird list date format'
    postingbodies = html.xpath('id("postingbody")')
    if len(postingbodies) > 0:
        postingbody = postingbodies[0].text_content()
    else:
        warnings.warn('No #postingbody found on the page')
        return None, None

    titles = html.xpath('//title')
    if len(titles) > 0:
        title = titles[0].text_content()
    else:
        warnings.warn('No <title /> found on the page')
        return None, None

    for text in [title, postingbody]:
        body = iter(text.split(' '))
        for window in _ngrams(body):
            d = list(dates_in_tokens(window))
            if len(d) == 2:
                return tuple(d)
            else:
                for i in range(1, len(window)):
                    if _is_end_date(window[0], window[1:i]):
                        return None, window[1:i]
    return None, None

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

def convert_date(listdate, year = datetime.date.today().year):
    if listdate == None or len(listdate) != 2:
        return None

    month, day = listdate
    digits = re.sub(r'[^0-9]', '', day)
    if digits == '':
        return None

    datestring = '%d|%s|%d' % (year, month, int(digits))
    try:
        return datetime.datetime.strptime(datestring, '%Y|%b|%d').date()
    except ValueError:
        return datetime.datetime.strptime(datestring, '%Y|%B|%d').date()

def convert_dates(dates_list, convert_date_func = convert_date):
    converted = list(filter(None, map(convert_date_func, dates_list)))
    if len(converted) != 2:
        return None
    return tuple(sorted(converted))

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

def humandate(text, html):
    ds = html.xpath('//p[text()="%s"]/time/@datetime' % text)
    if ds != []:
        e = dateutil.parser.parse(ds[0])
        return int(datetime.datetime.astimezone(e).timestamp())
