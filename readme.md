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
a [small suitcase](http://thomaslevine.com/!/stuff-2014-02).
Thus, I am able to make full use of these
short-term sublets of externally imposed duration. So I'm going
to search Craigslist for these sublets and then sublet them.

## How to
Set proxyies if you please, either with environment variables

    export http_proxy=tlevine:hohraoeuaoeu@example.com:8080

or in `config.py`. (See the [example](config.py.example).)

Then run like so.

    ./main.py

## To do
Maybe I should distinguish between two sorts of lengths.

* Renter is going away and then coming back (about a month)
* Renter wants someone else to finish the lease (about half a year)

Also, extract these features

* Furnished or not
* Has laudnry
* Is it available because the person is going away for a short trip?
* Is it available because the person is moving and has to finish the lease?
* Is it available because a new person is moving in but not for a couple weeks?
* Datetime posted
* Datetime updated
