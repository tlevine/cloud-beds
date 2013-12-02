'Train this on the fixtures.'
import os

import lxml.html
import pandas

df = pandas.read_csv(os.path.join('fixtures','fixtures.csv')).head()
df.index = df['url'].map(lambda url: int(url.split('/')[-1].split('.')[0]))
df['filename'] = df['url'].map(lambda url: os.path.join('fixtures',url.split('/')[-1]))
df['html'] = df['filename'].map(lambda x: lxml.html.parse(x).getroot())
