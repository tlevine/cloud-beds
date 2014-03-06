import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def db(url):
    engine = sa.create_engine(url)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind = engine)
    session = Session()

    return session
    while True:
        result = (yield)
        session.add(Listing(**result))
        session.commit()

class Listing(Base):
    __tablename__ = 'listing'

    url = sa.Column('url', sa.Text, primary_key = True)

    site = sa.Column('site', sa.Text)
    section = sa.Column('section', sa.Text)
    title = sa.Column('title', sa.Text)

    posted = sa.Column('posted', sa.DateTime)
    updated = sa.Column('updated', sa.DateTime)
    downloaded = sa.Column('downloaded', sa.DateTime)

    price = sa.Column('price', sa.Integer)
    longitude = sa.Column('longitude', sa.Float)
    latitude = sa.Column('latitude', sa.Float)

    html = sa.Column('html', sa.Text)
