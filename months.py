'A stupid approach to date testing.'
import re
import itertools

def getmonthnames():
    months = [
        'january','february','march','april',
        'may','june','july','august',
        'september','october','november','december',
    ]
    return dict(zip(months + [month[:3] for month in months], itertools.chain(range(1, 13), range(1, 13))))
months = getmonthnames()

def tokenize(text):
    return filter(None, re.split(r'\W', text))

def start_end(text):
    xs = sorted((months[word] for word in set(tokenize(text)) if word.lower() in months))
    if len(xs) == 0:
        return None
    elif len(xs) == 1:
        return xs[0], xs[0]
    else:
        return xs[0], xs[-1]
