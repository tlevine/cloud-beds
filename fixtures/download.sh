#!/bin/sh
for fixture in $(cat fixtures.csv|sed 1d|cut -d, -f1); do
  filename=$(echo $fixture | sed 's/^.*\///')
  wget -O $filename $fixture
  sleep $(( $RANDOM / 1000 ))
done
