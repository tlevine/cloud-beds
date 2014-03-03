import sqlalchemy as
import sqlalchemy.orm as orm


DATABASES = [
    'sqlite://///cloud-sleeping.db',
]




def db(databases = DATABASES):
    sessions = {database:session(database) for database in databases}
    while True:
        result = (yield)
        for session in sessions.values():
            session

def session(database):
    engine = {database:sa.create_engine(database)
    Session = orm.sessionmaker(bind = engine)
    return Session()

class Listing(sa.Table):
    url = sa.Column('url', sa.Text, primary_key = True),

    site = sa.Column('url', sa.Text),
    section = sa.Column('section', sa.Text),
    title = sa.Column('title', sa.Text),

    posted = sa.Column('posted', sa.DateTime),
    updated = sa.Column('updated', sa.DateTime),
    downloaded = sa.Column('downloaded', sa.DateTime),

    price = sa.Column('price', sa.Integer),
    longitude = sa.Column('longitude', sa.Float),
    latitude = sa.Column('latitude', sa.Float),

    html = sa.Column('html', sa.Text),
