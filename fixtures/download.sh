#!/bin/sh
for fixture in $(cat fixtures.csv|sed 1d|cut -d, -f1); do
  filename=$(echo $fixture | sed 's/^.*\///')
  if ! test -e $filename; then
    echo Beginning download of $fixture
    wget --header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0' -O $filename $fixture
    echo Finished downloading $fixture
    sleep $(( $RANDOM / 1000 ))
  fi
    echo Already downloaded $fixture
done
