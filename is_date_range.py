'Train this on the fixtures.'
import os

import lxml.html
import pandas

df = pandas.read_csv(os.path.join('fixtures','fixtures.csv'))
df['filename'] = df['url'].map(lambda url: os.path.join('fixtures',url.split('/')[-1]))
df['html'] = df['filename'].map(lambda x: lxml.html.parse(x).getroot())
