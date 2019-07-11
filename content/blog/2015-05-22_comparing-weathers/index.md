+++
title = "Comparing weathers in places I've lived"
description = "Looking how they differ by data"
category = "Data science"
tags = ["python", "notebook"]
+++


```python
%matplotlib inline

import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn  # make charts prettier and more readable
```


```python
# Let's load one of the CSV to see what they look like
nice = pd.read_csv('nice.csv')
nice[:5]
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>month</th>
      <th>avg_temp</th>
      <th>min_temp</th>
      <th>max_temp</th>
      <th>humidity</th>
      <th>rainfall</th>
      <th>raindays</th>
      <th>snowdays</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>01-2011</td>
      <td>8.6</td>
      <td>4.8</td>
      <td>12.4</td>
      <td>67.0</td>
      <td>2.9</td>
      <td>5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>02-2011</td>
      <td>9.3</td>
      <td>7.1</td>
      <td>11.1</td>
      <td>69.1</td>
      <td>2.9</td>
      <td>5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>03-2011</td>
      <td>11.7</td>
      <td>7.8</td>
      <td>14.3</td>
      <td>67.0</td>
      <td>3.9</td>
      <td>5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>04-2011</td>
      <td>15.6</td>
      <td>13.3</td>
      <td>18.5</td>
      <td>67.4</td>
      <td>0.4</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>05-2011</td>
      <td>19.7</td>
      <td>16.6</td>
      <td>24.8</td>
      <td>60.6</td>
      <td>0.0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>



We can see the shape of our CSV files.
There are 8 columns, all pretty explicit and containing the average for the month in column month except for raindays and snowdays which contains the number of days in that month where it rained and snowed respectively.

Note: I currently count raindays as the number of days where the rainfall is above 5mm (which is completely arbitrary).
If you look at the website I scraped it does contain a column for rain days  but some days are marked as rain days when there is no rainfall and the reverse.
Even then it's not really accurate as I'm only interested in quality of life and rain at 4am is not annoying lots of people.

Cool. Let's try plotting something first to see if everything is okay and load the other cities.



```python
_ = nice['avg_temp'].plot(figsize=(15, 5))
```


{{ image(src="weather_3_0.png", alt="Average temperature in Nice") }}


While we could continue having one `DataFrame` per city, it is more convenient to have one `DataFrame` containing all the data as this allows us to use plotting directly from it like we did above.


```python
locations = ['nice', 'montreal', 'okinawa', 'london']
weather = pd.DataFrame()

for location in locations:
    frame = pd.read_csv('%s.csv' % location)
    # We need to keep track of where it's coming from obviously
    frame['location'] = location
    weather = weather.append(frame)

# Alternative to using slicing
weather.head()
```


<div class="contained" style="max-height:1000px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>month</th>
      <th>avg_temp</th>
      <th>min_temp</th>
      <th>max_temp</th>
      <th>humidity</th>
      <th>rainfall</th>
      <th>raindays</th>
      <th>snowdays</th>
      <th>location</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>01-2011</td>
      <td>8.6</td>
      <td>4.8</td>
      <td>12.4</td>
      <td>67.0</td>
      <td>2.9</td>
      <td>5</td>
      <td>0</td>
      <td>nice</td>
    </tr>
    <tr>
      <th>1</th>
      <td>02-2011</td>
      <td>9.3</td>
      <td>7.1</td>
      <td>11.1</td>
      <td>69.1</td>
      <td>2.9</td>
      <td>5</td>
      <td>0</td>
      <td>nice</td>
    </tr>
    <tr>
      <th>2</th>
      <td>03-2011</td>
      <td>11.7</td>
      <td>7.8</td>
      <td>14.3</td>
      <td>67.0</td>
      <td>3.9</td>
      <td>5</td>
      <td>0</td>
      <td>nice</td>
    </tr>
    <tr>
      <th>3</th>
      <td>04-2011</td>
      <td>15.6</td>
      <td>13.3</td>
      <td>18.5</td>
      <td>67.4</td>
      <td>0.4</td>
      <td>1</td>
      <td>0</td>
      <td>nice</td>
    </tr>
    <tr>
      <th>4</th>
      <td>05-2011</td>
      <td>19.7</td>
      <td>16.6</td>
      <td>24.8</td>
      <td>60.6</td>
      <td>0.0</td>
      <td>0</td>
      <td>0</td>
      <td>nice</td>
    </tr>
  </tbody>
</table>
</div>



We can also use `.describe()` on a `DataFrame` instead of doing `.median()`, `.sum()` etc on every single column to have a quick overview of all the variables.


```python
weather.describe()
```


<div class="contained" style="max-height:1000px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>avg_temp</th>
      <th>min_temp</th>
      <th>max_temp</th>
      <th>humidity</th>
      <th>rainfall</th>
      <th>raindays</th>
      <th>snowdays</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>192.000000</td>
      <td>192.000000</td>
      <td>192.000000</td>
      <td>192.000000</td>
      <td>192.000000</td>
      <td>192.000000</td>
      <td>192.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>14.698437</td>
      <td>9.718750</td>
      <td>19.635937</td>
      <td>70.260937</td>
      <td>3.507292</td>
      <td>4.843750</td>
      <td>2.114583</td>
    </tr>
    <tr>
      <th>std</th>
      <td>9.001405</td>
      <td>11.141769</td>
      <td>7.269971</td>
      <td>7.409749</td>
      <td>3.491553</td>
      <td>3.241834</td>
      <td>5.640857</td>
    </tr>
    <tr>
      <th>min</th>
      <td>-10.000000</td>
      <td>-24.900000</td>
      <td>1.600000</td>
      <td>54.200000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>9.150000</td>
      <td>4.650000</td>
      <td>13.950000</td>
      <td>65.300000</td>
      <td>1.400000</td>
      <td>2.750000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>16.250000</td>
      <td>11.950000</td>
      <td>20.950000</td>
      <td>69.750000</td>
      <td>2.700000</td>
      <td>5.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>21.025000</td>
      <td>16.600000</td>
      <td>25.225000</td>
      <td>74.800000</td>
      <td>3.900000</td>
      <td>7.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>29.600000</td>
      <td>28.400000</td>
      <td>30.700000</td>
      <td>87.500000</td>
      <td>22.000000</td>
      <td>15.000000</td>
      <td>25.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Define some styles that we will reuse for all line graphs
styles = {
    'london': 'go-',
    'nice': 'ro-',
    'montreal': 'bo-',
    'okinawa': 'co-',
}

# we define a method since we will need to do that pretty often
def plot_grouped_by(dataframe, column_name):
    """Plots the dataframe grouped by location for the given column"""
    # Need to use the month as the index
    locations = dataframe.set_index('month').groupby('location')

    for loc_name, loc in locations:
        loc[column_name].plot(x='month', label=str(loc_name), style=styles[str(loc_name)])


plt.figure(figsize=(16, 8))
ax = plt.subplot(111)

plot_grouped_by(weather, 'avg_temp')

# Yes, I did add the 40 degrees tick just to be able to fit the legend properly
plt.yticks([-15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 40], fontsize=14)
plt.legend(fontsize=14, loc="upper left")
plt.title("Monthly average temperature 2011-2014", fontsize=16)
_ = plt.ylabel("Temperature (celsius)", fontsize=16)
_ = plt.xlabel("Time", fontsize=16)
```


{{ image(src="weather_8_0.png", alt="Monthly average temperatures") }}


We can make a few observations on this chart:

- Montreal has the biggest variance in temperature throughout the year: from very cold in winter to quite warm in summer
- London is disappointingly average and is missing at least 10° on its summer time for my taste
- Okinawa is hot, even winter is warmer than London's summer most of the time
- Nice has a nice weather, hot in summer but not too cold in winter

For the next plots, let's focus on 2014 only in order to have an idea on how a year looks like in those cities.


```python
# Making sure we have a datetime first rather than a string
weather['month'] = pd.to_datetime(weather['month'], format="%m-%Y")
start = datetime.date(2014, 1, 1)

# pandas allows all kind of iterator magic
weather_2014 = weather[weather.month >= start]
weather_2014.head()
```




<div class="contained" style="max-height:1000px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>month</th>
      <th>avg_temp</th>
      <th>min_temp</th>
      <th>max_temp</th>
      <th>humidity</th>
      <th>rainfall</th>
      <th>raindays</th>
      <th>snowdays</th>
      <th>location</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>36</th>
      <td>2014-01-01</td>
      <td>9.7</td>
      <td>6.4</td>
      <td>12.4</td>
      <td>71.6</td>
      <td>9.2</td>
      <td>11</td>
      <td>0</td>
      <td>nice</td>
    </tr>
    <tr>
      <th>37</th>
      <td>2014-02-01</td>
      <td>9.9</td>
      <td>6.8</td>
      <td>13.4</td>
      <td>69.6</td>
      <td>4.6</td>
      <td>7</td>
      <td>0</td>
      <td>nice</td>
    </tr>
    <tr>
      <th>38</th>
      <td>2014-03-01</td>
      <td>12.5</td>
      <td>7.4</td>
      <td>15.4</td>
      <td>62.3</td>
      <td>2.7</td>
      <td>3</td>
      <td>0</td>
      <td>nice</td>
    </tr>
    <tr>
      <th>39</th>
      <td>2014-04-01</td>
      <td>15.3</td>
      <td>13.2</td>
      <td>17.3</td>
      <td>69.3</td>
      <td>0.3</td>
      <td>0</td>
      <td>0</td>
      <td>nice</td>
    </tr>
    <tr>
      <th>40</th>
      <td>2014-05-01</td>
      <td>17.5</td>
      <td>14.4</td>
      <td>20.2</td>
      <td>64.1</td>
      <td>0.6</td>
      <td>1</td>
      <td>0</td>
      <td>nice</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Let's look at temperatures and humidity
plt.figure(figsize=(16, 8))

# this 221 means we want a 2x2 plots display and this is the first one
# (so upper left)
ax = plt.subplot(221)

plot_grouped_by(weather_2014, 'avg_temp')
plt.yticks([-15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35], fontsize=14)
plt.legend(fontsize=14, loc="lower center")
plt.title("Monthly average temperature 2014")
_ = plt.ylabel("Temperature (celsius)", fontsize=16)

ax2 = plt.subplot(222)

plot_grouped_by(weather_2014, 'max_temp')
plt.yticks([0, 10, 20, 30, 40], fontsize=14)
plt.legend(fontsize=14, loc="lower center")
plt.title("Max temperature 2014")
_ = plt.ylabel("Temperature (celsius)", fontsize=16)

ax3 = plt.subplot(223)

plot_grouped_by(weather_2014, 'min_temp')
plt.yticks([-30, -20, -10, 0, 10, 20, 30], fontsize=14)
plt.legend(fontsize=14, loc="lower center")
plt.title("Min temperature 2014")
_ = plt.ylabel("Temperature (celsius)", fontsize=16)

ax4 = plt.subplot(224)

plot_grouped_by(weather_2014, 'humidity')
plt.title("Average monthly humidity % in 2014 (legend identical)")
_ = plt.ylabel("Humidity %", fontsize=16)

```


{{ image(src="weather_11_0.png", alt="Graph comparing 4 cities") }}


Looking at those graphs we can notice a few things:

- Montreal winter is pretty damn cold but is not really humid, which makes it not THAT bad and Canadians know how to do proper insulation. Summer is quite nice all around, nice temperatures and pretty dry.
- Nice is good all year round, it sometimes gets below 10° but never reaches 0° while being dry. Having grown up there I feel like I have been spoiled when it comes to weather.
- London is average but we can see the winter is very humid, which is the reason why I feel colder when it's 0° in London than -15° in Montreal.
- Okinawa looks really good until you experience that summer humidity. For those that haven't lived in a tropical climate, it means that you are sweating an awful lot very quickly and air con is a necessity.

To finish this notebook, let's have a look at the rain and snow data.



```python

colors = {
    'london': 'green',
    'nice': 'red',
    'montreal': 'blue',
    'okinawa': 'cyan',
}

def bar_plot(ax, column_name):
    weather_2014.set_index(
        ['month', 'location']
    ).unstack().plot(
        ax=ax,
        kind='bar',
        y=column_name
    )

plt.figure(figsize=(16, 8))
ax = plt.subplot(211)

bar_plot(ax, "raindays")
plt.legend(fontsize=14, loc="best")
plt.title("Rain days per month in 2014")
_ = plt.ylabel("Number of rain days", fontsize=16)

ax2 = plt.subplot(212)

bar_plot(ax2, "snowdays")
plt.legend(fontsize=14, loc="best")
plt.title("Snow days per month in 2014")
_ = plt.ylabel("Number of snow days", fontsize=16)
```


{{ image(src="weather_13_0.png", alt="Rain and snow days") }}


We can see it's raining quite a bit in Okinawa since they have a rainy season (May-June) and a typhoon season (June-November).
Nice is probably the nicest, having close to no rains during summer.
When it comes to snow, Montreal is the only contender as snow in Nice and London is very rare and it hasn't snowed in Okinawa for over 30 years.


While weather is only one of the elements that are necessary to consider when moving (along with salary, atmosphere, friends/family etc.), it is one of the most important thing for me.
If I had to make a ranking of those cities on a weather basis, it would be:

1. Nice
2. Montreal
3. Okinawa/London

Okinawa and London are tied for completely different reasons: one has the legendary British weather and its 2 weeks of summer and the other is so hot and humid that it can be hard to breath at times (but you get amazing sea and beaches).
Now that you have seen how to use Pandas (for those that had never tried it before), it's up to you to finds things to compare. Do share them when you do as it is always interesting to read.
