.PHONY: fixtures

all: schema
	./index.py

fixtures:
	cd ./fixtures && ./download.sh

schema:
	sqlite3 craigslist.sqlite < schema.sql
