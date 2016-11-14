+++
title = "Finding trending things in Elasticsearch using python and redis"
slug = "finding-trending-things"
url = "finding-trending-things"
description = "How to calculate trendiness factor from ES and use it in queries"
date = "2014-09-19"
categories = ["programming"]
tags = ["elasticsearch", "python"]
+++

One of the features at my current contract is displaying widgets showing trending news articles.  
We define trendiness on a company basis (topic as well but let's keep it to only companies for this article), ie we want to display articles from companies that are trending.  
The articles are stored in [Elasticsearch](http://www.elasticsearch.org/) and we want to spot the trending ones for a given time period (last week, last month, last quarter, last year).  
For each article we keep track (in the article doc in ES, as a [nested type](http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-nested-type.html)) of the companies mentioned and we use that field to calculate the trends (this is a bit simplified, there is actually a second similar field as well but let's keep things simple for the sake of the article).  

These trending articles are shown in a iframe and this iframe had been timing out even for short-ish time periods (3 months or so) worth of data.  
Since we can't really have things timing out, I decided to have a look and try to improve things.   

## What was there before
Looking at the code, I realised that the current trending code was very naive.  
It was working in two steps:

- gets the number of times a company was mentioned over the time period we're interested in
- run a javascript script in a ES query that was calculating the score for each article by adding the score for of each company in the article 

There are two things wrong with that approach.  
The first obvious one is that it massively favours big companies, as they will have more articles talking about them, and even if they are actually trending down compared to the norm, they will still be at the top of the trending list.  
The second one is that it is running a script iterating over 2 dicts for each article (2 because as mentioned in the introduction, there is another field we rate with in addition to companies), making it pretty damn slow and timing out on the live server.  

## A new approach
With these 2 things in mind, I set out to figure out a better and faster way to find the trending companies.  

### Trendiness
The first thing to define is trendiness: something trendy is something that is mentioned more often than usual.  
From that definition we can realise that we first need to define what is _usual_, also called the *baseline* so let's start with that.

### Defining a baseline using Elasticsearch
As mentioned above, the goal in defining a baseline is finding out what's normal for a company.  
I chose to find the number of mentions for each company everyday for the 3 months prior to the interval we're interested in.  
3 months is a completely arbitrary value that could as well be 1 month but it seemed about right.  
Elasticsearch provides a [date histogram aggregation](http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-aggregations-bucket-datehistogram-aggregation.html) that does exactly that !  

Let's have a look at a query, there are a few options worth mentioning:

```json
{
    "size": 0,
    "query": {...},
    "aggs": {
        "companies": {
            "date_histogram": {
                "field": "harvest_date",
                "interval": "day",
                "format": "yyyy-MM-dd",
                "min_doc_count": 0, 
                "extended_bounds": {
                    "min": history_start,
                    "max": end
                },
            },
            "aggs": {
                "nested_items": {
                    "aggs": {
                        "items": {
                            "terms": {
                                "field": "companies.id",
                                "size": 0
                            }
                        }
                    },
                    "nested": {
                        "path": "companies"
                    }
                }
            }
        }
    }
}

```
As mentioned in the introduction, companies is a nested type so require some addition levels in the queries.  
There are a few things to note:

- we want a day by day interval, ES provides that out of the box and a few more if necessary, see the link above for all the possibilities
- we want the date formatted as ISO for simplicity sake
- we want to get as many buckets as possible so we even get the days where we don't have any matching documents by setting **min_doc_count** to 0
- we want every possible day between history_start and end to have a bucket by setting the **extended_bounds** min/max to these dates

With this query we get a bucket for each day that can contain companies with they doc_count if there are, or an empty bucket otherwise.  
With all the companies ids and that data, we can recreate the complete histogram of the number of article for each company in our postgres  database.  I also separate the history data from the window we are observing, the python code looks something like:

```python
AggregationData = namedtuple('AggregationData', ['history', 'window'])

def _get_numbers_by_day(all_ids, aggregation, window_start):
  """window_start is ISO formatted string"""
  values = defaultdict(lambda: AggregationData([], []))
  
  in_window = False
  for day in aggregation:
    if not in_window:
      # remember we asked for the dates from the agg to be ISO formatted as well
      in_window = window_start == day['key_as_string']

    # then look if we got doc_counts for that day, add it to the right tuple in the values dict, see below
    # fill with 0 for the rest, for example
    # (_id would have been set while looping over the ids not seen in the buckets here)
    if in_window:
      values[_id].window.append(0)
    else:
      values[_id].history.append(0)
    
```

We now have the data for all companies for each day. Cool.  


### Finding the trends

#### First approach
The first thing I tried was to get the mean value of the history values and divide the window period values with that mean to get normalized values compared to their usual values.  
You are then able to spot unusual activities when a value is above 1 (by that mean I something like 5, not 1.1) and identify trends by looking at the difference between 2 consecutive points: if the numbers are going up and are reasonably higher than 1, it's trending !  

While this gives _ok_ results, this approach fails to account for the standard deviation which can change the results quite a bit.  

#### Z-Score
Time to look at [z-score](http://en.wikipedia.org/wiki/Standard_score) !  
This is the standard algorithm to find trending things and is simple to implement :
![z-score formula](http://upload.wikimedia.org/math/8/4/6/8463971a22cc96a1e0612588e5656bce.png) with μ being the history mean and σ the standard deviation of the history data.  

Let's implement it quickly in python:

```python
from math import sqrt

def zscore(data, point):
  """Going to observe a single point here"""
  length_data = float(len(data)) # need floats, and we are using it several times
  mean = sum(data) / length_data  # and be careful of len(data) == 0
  std = sqrt(sum((point - mean) ** 2 for point in data) / length_data)
  
  # And we now apply the formula above
  return (point - mean) / std  # again, check for std == 0
```
Nothing fancy going there, just getting the mean and standard deviation for the data and use the formula.  
This gives pretty good results (good thing we humans can detect if something is trendy pretty easily):

```bash
print zscore([20, 10, 10, 5, 5, 6, 6, 6], 20)
>> 2.4244128728
print zscore([0, 2, 3, 4, 6, 8], 2)
>> -0.7027642215
```

There is one issue with that though:

```python
print zscore([20, 20, 20, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0], 20)
>> 1.15470053838
print zscore([0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 20, 20, 20, 20], 20)
>> 1.15470053838
```
Our guts tell us that the first one is more unusual than the second one and thus should have a higher rating than the second (imagine similar series containing hundred of points rather than this small example) if we are only looking at the last few days.  
When we are looking at trending things, recent values are more important than old ones right?  
We need to somehow depreciate the previous values as we move forward in the history.  
This is called a rolling zscore and unfortunately Pandas doesn't [have one for zscore](http://pandas.pydata.org/pandas-docs/stable/api.html#standard-moving-window-functions).  I could have probably used rolling_apply but where would be the fun in that and it is pretty easy to implement anyway !

#### Rolling z-score
We got the formula and the code for the normal z-score above.  
By rolling we mean that we re-apply the formula for every point, and in our case adding a factor so that the oldest points carry the less value.  
How do we do that?  
Simply by multiplying the average by a factor for every point.  
An implementation in python looks like the following (maths taken from [that stackoverflow answer](http://stackoverflow.com/a/826509):  

```python
def rolling_zscore(data, observed_window, decay=0.9):
    """
    The lowest the decay, the more important the new points
    Decay is there to ensure that new data is worth more than old data
    in terms of trendiness
    """
    # Set the average to a the first value of the history to start with
    avg = float(data[0])
    squared_average = float(data[0] ** 2)

    def add_to_history(point, average, sq_average):
        average = average * decay + point * (1 - decay)
        sq_average = sq_average * decay + (point ** 2) * (1 - decay)
        return average, sq_average

    def calculate_zscore(average, sq_average, value):
        std = round(sqrt(sq_average - avg ** 2))
        if std == 0:
            return value - average

        return (value - average) / std

    for point in data[1:]:
        avg, squared_average = add_to_history(point, avg, squared_average)

    trends = []
    # We recalculate the averages for each new point added to be more
    # accurate
    for point in observed_window:
        trends.append(calculate_zscore(avg, squared_average, point))
        avg, squared_average = add_to_history(point, avg, squared_average)

    # Close enough way to find a trend in the window
    return sum(trends) / len(trends) if len(trends) != 0 else 0
```

Let's see the results and how decay affects the trendiness by checking the values for the trends list:  

```python
# Values used, you can see data averaging 3-4
data = [0, 0, 3, 5, 4, 3, 6, 0, 2, 6, 8, 9, 0, 1, 3, 7, 5, 6, 4, 5, 0, 1, 3, 5, 0, 6, 4, 2, 3, 1]
window_not_trending = [3, 4, 3, 0, 1, 4, 5]
window_trending = [5, 8, 10, 12, 15, 17, 20]

print rolling_zscore(data, window_not_trending)
[3.8618524915490227e-05, 0.5000347566724239, -0.04996871899481836, -1.5449718470953364, -0.8904746623858029, 0.6985728038527774, 1.1287155234674997]
>> -0.0225790751369

print rolling_zscore(data, window_trending)
[1.0000386185249155, 2.400034756672424, 2.106687520670121, 2.5626854352697754, 2.4798126688070985, 2.185465121541111, 2.566918609387]
>> 2.18594896155

# And now with diferent decay, not linear relation
print rolling_zscore(data, window_trending, decay=0.5)
>> 1.85740988579
print rolling_zscore(data, window_trending, decay=0.1)
>> 2.93406854599

```
And now let's see the results for the type of series we had before that would cause problems:

```python
print rolling_zscore([20, 20, 20, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [20])
>> 2.03674495279
print rolling_zscore([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 20, 20, 20, 20], [20])
>> 1.062882
```

Ok we got something that looks like credible results, time to get back to the ES part but first, a (very) quick trip to redis.

### Finding the most trendings in that
So we got a dict with companies ids as keys and trendiness as values.  
We could easily sort that in python but where's the fun in that !  
Redis provides a sorted set for us that we can query easily as we want and since we want to cache things to avoid repeating all these calculations and the initial ES query, let's use that: [ZADD](http://redis.io/commands/zadd).  
The syntax is a bit odd (to me) as you five the value before the key, but is easy to use:

```python
# This will insert a member to the set `company_key`,
# with the rolling average as the value and the company_id as they key
for company_id, agg in companies.iteritems():
    redis.zadd(company_key, rolling_zscore(agg.history, agg.window), company_id)
```

Now, if we query redis for that set, it will return the key-value tuple sorted the way we want:

```python
# This asks for the 5 companies with the highest trending score
# and to send the score back as well
# if you want to find the 5 lowest trending companies, you would use redis.zrange
trending_companies = redis.zrevrange(company_key, 0, 5, withscores=True)
```

### Wrapping this up in Elasticsearch
Note: I am a newbie with ES, so do let me know if there are better ways to do that
We got our trending companies, time to actually take them into articles when fetching data from ES.  
ES provides a way to [boost](http://www.elasticsearch.org/guide/en/elasticsearch/reference/1.x/query-dsl-boosting-query.html) a query, which will change a document score (ie 0.2 boost means its the document score is multiplied by 0.2 and so has a lower score while a boost of 1.5 means it will be higher than normal).  
Good thing we have the trendiness of every companies ! We can just give each company its trendiness as a boost:

```python
companies_filters = []
# trending_companies if the list of tuples returned by redis.zrevrange
for company in trending_companies:
    companies_filters.append({
        "filter": {
            "nested": {
                "path": "companies",
                "filter": {
                    "term": {
                        "companies.id": company[0]  # id
                    }
                }

            }
        },
        "boost_factor": 1 + company[1]  # score (can be negative)
    })
```
From that we get a list of filters to apply to our query that will favour articles from the trendy companies.  

## Conclusion
I finally got to play a bit with Elasticsearch and it looks quite good !  
Being able to do queries in JSON (still more complex than SQL imo) and easy to compose it from different functions as from the python side we are just manipulating a dict.  
I'll definitely use it when I need search on another project.
