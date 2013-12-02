#!/bin/sh
for fixture in $(cat fixtures.csv|sed 1d|cut -d, -f1); do
  echo $fixture
done
