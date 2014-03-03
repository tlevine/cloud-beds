#!/bin/sh
set -e
for fixture in $(cat fixtures.csv|sed 1d|cut -d, -f1); do
  filename=$(echo $fixture | sed 's/^.*\///')
  if ! test -e $filename; then
    echo Copying $fixture
    cp ../craigslist/$(echo "$fixture"|sed 's+https\?://++') .
  fi
done
