'Train this on the fixtures.'
import os

import lxml.html
import pandas

def main():
    df = pandas.read_csv(os.path.join('fixtures','fixtures.csv')).head()
    df.index = df['url'].map(lambda url: int(url.split('/')[-1].split('.')[0]))
    df['filename'] = df['url'].map(lambda url: os.path.join('fixtures',url.split('/')[-1]))
    df['html'] = df['filename'].map(lambda x: lxml.html.parse(x).getroot())

def is_date(tokens: list): -> bool
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
