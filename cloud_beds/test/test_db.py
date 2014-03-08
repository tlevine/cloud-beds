import nose.tools as n

from cloud_beds.db import db, Listing

class FakeSession:
    def __init__(self):
        self._added = []
        self._flushed = 0
    def query(self, cls):
        n.assert_equal(cls, Listing)
        return FakeQuery()
    def add(self, obj):
        n.assert_is_instance(obj, Listing)
        self._added.append(obj)
    def flush(self):
        self._flushed += 1

class FakeQuery:
    def get(self, pk):
        if pk == 'http://example.com':
            return ['Pretend this is a result.']

def test_db_no_save():
    session = FakeSession()
    sink = db(session = session)

    result = {
        'url': 'http://example.com',

        'site': None,
        'section': None,
        'title': None,

        'posted': None,
        'updated': None,
        'downloaded': None,

        'price': None,
        'longitude': None,
        'latitude': None,

        'html': None,
    }

    sink.send(result)
    n.assert_equal(session._flushed, 1)
    n.assert_equal(session._added, [Listing(result)])

def test_db_save():
    session = FakeSession()
    sink = db(session = session)

    result = {
        'url': 'http://this.is.a.new.website.example.com',

        'site': None,
        'section': None,
        'title': None,

        'posted': None,
        'updated': None,
        'downloaded': None,

        'price': None,
        'longitude': None,
        'latitude': None,

        'html': None,
    }

    sink.send(result)
    n.assert_equal(session._flushed, 0)
    n.assert_equal(session._added, [])
