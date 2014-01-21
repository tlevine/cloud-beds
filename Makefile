.PHONY: fixtures
date := $(shell date +'%Y-%m-%dT%I:%M:%S')

all: schema
	./index.py

fixtures:
	cd ./fixtures && ./copy.sh

schema:
	sqlite3 craigslist.sqlite < schema.sql

clean:
	sqlite3 craigslist.sqlite 'DROP TABLE results;'

/tmp/craigslist.sqlite:
	test -f craigslist.sqlite && \
	( ! test -h craigslist.sqlite ) && \
	cp craigslist.sqlite /tmp/craigslist.sqlite && \
	mv craigslist.sqlite craigslist.sqlite.$(date) && \
	ln -s /tmp/craigslist.sqlite .

/tmp/craigslist:
	test -d craigslist && \
	( ! test -h craigslist ) && \
	cp -R craigslist /tmp && \
	mv craigslist craigslist.$(date) && \
	ln -s /tmp/craigslist .

tmp: /tmp/craigslist.sqlite /tmp/craigslist

save: tmp
	test -h craigslist && rm craigslist
	test -h craigslist.sqlite && rm craigslist.sqlite
	mv /tmp/craigslist.sqlite .
	mv /tmp/craigslist .
