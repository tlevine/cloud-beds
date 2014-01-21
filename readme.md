Finding undervalued short-term sublets
======
I search Craigslist to find low-priced short-term sublets.
And then I sublet them.

## Hypothesis
If one is going to be away from his apartment for a few weeks,
it might make sense for him to sublet his apartment for those weeks.
While you can probably find someone who would take the apartment
for approximately the right time-span, it's probably hard to find
someone who wants exactly the time-span you propose. A person
who is subletting an apartment for a specific period of duration
on the order of a month is likely to accept less than a typical
month of rent.

## Idea
All of the objects that I care to have with me regularly fit in
a suitcase and a backpack. In fact, I could probably get it down
to just a backpack; I only need the suitcase because it contains
a desk and a monitor. Thus, I am able to make full use of these
short-term sublets of externally imposed duration. So I'm going
to search Craigslist for these sublets and then sublet them.

## 3Taps Documentation
The [official documentatio](http://docs.3taps.com/) is great, except
that. Basic things like a list of the sources that 3Taps has, a list
of categories, &c. are in the [reference API](http://docs.3taps.com/reference_api.html).

[These slides](http://www.slideshare.net/devinfoley/3taps-apis)
have one example query, on slide 7.

This [PHP client](https://github.com/cookieflow/3taps-php-client)
has some vaguely helpful documentation.

### Finding sublets
The code is `RSUB`.

    $ http "http://reference.3taps.com/categories?auth_token=$APIKEY"
    ...
        {
            "code": "RSUB", 
            "group_code": "RRRR", 
            "group_name": "Real Estate", 
            "name": "Housing Sublets"
        }, 
    ...

With queries like this, you can eventually figure out the location code of interest.
But that's not too much of an issue just yet.

    http "http://reference.3taps.com/locations?auth_token=$APIKEY&state=USA-NY&level=city"

It seems like craigslist is the only source for New York City, so let's stick with that for now.

## Longish
Maybe I should distinguish between two sorts of lengths.

* Renter is going away and then coming back (about a month)
* Renter wants someone else to finish the lease (about half a year)


## Stuff

    sed 1d /tmp/short-term-sublets.tsv |sort -n|head

3Taps stuff is cached in `3taps`; delete that to refresh the 3Taps cache.


## Regions

        nyc_regions = list(map(lambda x:'USA-NYM-'+x, ['BRO','MAN','QUE']))
        dc_regions = ['USA-WAS-DIS', 'USA-WAS-BAL']
        chicago_regions = ['USA-CHI-CIT']
        regions = chicago_regions # nyc_regions + dc_regions + chicago_regions

## Nice queries
The current month is January (1), so I searched until March (3).

```sql
select * from results where price < 500 and end <= 3 order by end-start, price;
```

```sql
select * from results where (start not null or end not null) and url like '%austin%' order by end-start; 
```
```sql
select * from results where (start not null or end not null) and url like '%austin%' and url not glob '*/sbw/*' order by end-start;
```

```sql
select price, url, heading from results where (not super_bowl) and furnished and url like '%newyork%' and end = 2 and updated not null and posted not null order by (updated - posted)/(strftime('%s','now') - posted);
```

```sql
select price, url, heading from results where (not super_bowl) and furnished and url like '%newyork%' and end = 2 and updated not null and posted not null and price <= 1300 and (strftime('%s', 'now') - updated) < (1 * 24 * 3600) order by (updated - posted)/(strftime('%s','now') - posted);
```

## To do
Extract these features

* Furnished or not
* Has laudnry
* Is it available because the person is going away for a short trip?
* Is it available because the person is moving and has to finish the lease?
* Is it available because a new person is moving in but not for a couple weeks?
* Datetime posted
* Datetime updated


## How to
Clear the cache.

    make clean

Run everything.

    make

Browse results.

    sqlite3 craigslist.sqlite

Move things to `/tmp` it doesn't thrash the hard drive.

    make tmp

Move things back from `/tmp` so they persist.

    make save
