from craigsgenerator import craigsgenerator
import sqlalchemy

from config import proxies

DATABASES = [
    'sqlite://///cloud-sleeping.db',
]
TABLE = '''
CREATE TABLE IF NOT EXISTS listings (
  "url" TEXT NOT NULL,

  "site" TEXT NOT NULL,
  "section" TEXT NOT NULL,
  "title" TEXT NOT NULL,

  "posted" DATETIME NOT NULL,
  "updated" DATETIME,
  "downloaded" DATETIME NOT NULL,

  "price" INTEGER,
  "longitude" FLOAT,
  "latitude" FLOAT,

  "html" TEXT NOT NULL,
  UNIQUE("url")
);
'''

def main():
    cg = craigsgenerator(get = get, threads_per_section = 10, superthreaded = False,
        cachedir = os.path.join(os.environ['HOME'], 'dadawarehouse', 'craigslist'))

    sink = db()
    next(sink)

    for listing in cg:
        save(listing)

def get(url):
    return requests.get(url, proxies = proxies)

def db(targets = DATABASES):
    databases = {target:sqlalchemy.create_engine(target) for target in targets}
    for target in targets:
        target.execute(SCHEMA)
    while True:
        result = (yield)
        for target in targets:
            target.execute(
