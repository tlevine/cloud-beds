from craigsgenerator import craigsgenerator
import sqlalchemy

from config import proxies

DATABASES = [
    'sqlite://///cloud-sleeping.db',
]

def main():
    cg = craigsgenerator(get = get, threads_per_section = 10, superthreaded = False,
        cachedir = os.path.join(os.environ['HOME'], 'dadawarehouse', 'craigslist'))

    for listing in cg:
        save(listing)

def get(url):
    return requests.get(url, proxies = proxies)

def save(listing, targets = DATABASES):
    databases = {target:sqlalchemy.create_engine(target) for target in targets}
