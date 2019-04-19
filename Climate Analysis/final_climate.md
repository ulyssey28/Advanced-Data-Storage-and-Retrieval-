

```python
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
```


```python
import numpy as np
import pandas as pd
```


```python
import datetime as dt
```

# Reflect Tables into SQLAlchemy ORM


```python
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
```


```python
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
```


```python
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
```


```python
# We can view all of the classes that automap found
Base.classes.keys()
```




    ['measurement', 'station']




```python
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
```


```python
# Create our session (link) from Python to the DB
session = Session(engine)

```


```python

```


```python
#View of "measurement" table
pd.read_sql_table("measurement", engine).head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>station</th>
      <th>date</th>
      <th>prcp</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>USC00519397</td>
      <td>2010-01-01</td>
      <td>0.08</td>
      <td>65.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>USC00519397</td>
      <td>2010-01-02</td>
      <td>0.00</td>
      <td>63.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>USC00519397</td>
      <td>2010-01-03</td>
      <td>0.00</td>
      <td>74.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>USC00519397</td>
      <td>2010-01-04</td>
      <td>0.00</td>
      <td>76.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>USC00519397</td>
      <td>2010-01-06</td>
      <td>NaN</td>
      <td>73.0</td>
    </tr>
  </tbody>
</table>
</div>




```python

```


```python
#View of "station" table 
pd.read_sql_table("station", engine).head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>station</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>elevation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>USC00519397</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.2716</td>
      <td>-157.8168</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>USC00513117</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.4234</td>
      <td>-157.8015</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>USC00514830</td>
      <td>KUALOA RANCH HEADQUARTERS 886.9, HI US</td>
      <td>21.5213</td>
      <td>-157.8374</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>USC00517948</td>
      <td>PEARL CITY, HI US</td>
      <td>21.3934</td>
      <td>-157.9751</td>
      <td>11.9</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>USC00518838</td>
      <td>UPPER WAHIAWA 874.3, HI US</td>
      <td>21.4992</td>
      <td>-158.0111</td>
      <td>306.6</td>
    </tr>
  </tbody>
</table>
</div>




```python
# session.query(Station.station).all()
stations_list = []
stations_tup_list = session.query(Station.station).all()
for row in stations_tup_list:
    stations_list.append(row[0])
stations_list
```




    ['USC00519397',
     'USC00513117',
     'USC00514830',
     'USC00517948',
     'USC00518838',
     'USC00519523',
     'USC00519281',
     'USC00511918',
     'USC00516128']



# Exploratory Climate Analysis


```python
# Design a query to retrieve the last 12 months of precipitation data and plot the results

# Find the last date in the table:
# select the first row from the Measurement.date column (ordered in descending order based on date)
# Note the latest_date variable is currently a tuple with one item (a date string)
latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

"""
using a datetime class method we can transform our date string (first element of our latest_date tuple)
into a date object which allows us to better manipulate date values without being forced to hard-code 
"""
latest_date_obj = dt.date.fromisoformat(latest_date[0])

# Calculate the date 1 year ago from the last data point in the database
#use timedelta method perations to create a date object referencing a year from latest date
year_ago_from_latest = latest_date_obj - dt.timedelta(days=365)

# Perform a query to retrieve the date and precipitation scores
year_range_query = session.query(Measurement.date, Measurement.prcp).\
                              filter(Measurement.date.between(str(year_ago_from_latest), str(latest_date_obj))).order_by(Measurement.date)

# Save the query results as a Pandas DataFrame and set the index to the date column
precipication_df = pd.read_sql_query(year_range_query.statement, engine, index_col= "date")
precipication_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>prcp</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2016-08-23</th>
      <td>0.00</td>
    </tr>
    <tr>
      <th>2016-08-23</th>
      <td>0.15</td>
    </tr>
    <tr>
      <th>2016-08-23</th>
      <td>0.05</td>
    </tr>
    <tr>
      <th>2016-08-23</th>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2016-08-23</th>
      <td>0.02</td>
    </tr>
  </tbody>
</table>
</div>




```python

```


```python
precipication_df.plot()
plt.legend(loc="upper center")
plt.show()
```


![png](output_18_0.png)



```python

```


```python
# Use Pandas to calculate the summary statistics for the precipitation data
precipication_df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>prcp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2021.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>0.177279</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.461190</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>0.020000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.130000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>6.700000</td>
    </tr>
  </tbody>
</table>
</div>




```python

```


```python
# Design a query to show how many stations are available in this dataset?

# Query the count of station ids within the "station" table
station_count = session.query(func.count(Station.id)).all()
station_count
```




    [(9)]




```python

```


```python
# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.

"""
This query displays the station and count of measurement ids for each station
To do this, this query selects the Measurement.station and func.count(Measurement.id) from the "measurement" table...
grouped by stations in the Measurement.station column... 
ordered by the count of measurement ids in descending order 
"""

session.query(Measurement.station, func.count(Measurement.id)).\
                       group_by(Measurement.station).\
                                   order_by(func.count(Measurement.id).desc()).all()

```




    [('USC00519281', 2772),
     ('USC00519397', 2724),
     ('USC00513117', 2709),
     ('USC00519523', 2669),
     ('USC00516128', 2612),
     ('USC00514830', 2202),
     ('USC00511918', 1979),
     ('USC00517948', 1372),
     ('USC00518838', 511)]




```python

```


```python
# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature for the most active station?

"""
Building on the previous query, this query displays the min, max, and avg temperature per station
based on values grouped by station ... ordered by measurement id count

conceptually you hold the same grouping of table values from the previous query (i.e the func.count(Measurement.id) column
still exists), but you select and display different aggregates and order these aggregates based on count
"""
session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                       group_by(Measurement.station).\
                                   order_by(func.count(Measurement.id).desc()).first()
```




    (54.0, 85.0, 71.66378066378067)




```python

```


```python
# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station 

#create a variable that will hold the tuple with the name of the station with the most observations
#to obtain this tuple we can reference the query used to order stations by most obseravtions 
#simply select the Measurement.station in the first row (which corresponds to the station with the most obeservations)
mobs_station = session.query(Measurement.station).\
                       group_by(Measurement.station).\
                                   order_by(func.count(Measurement.id).desc()).first()


#create a variable that will hold the date for the station with the most 
# Note the mobs_latest_date variable is currently a tuple with one item (a date string)
mobs_latest_date = session.query(Measurement.date).filter(Measurement.station == mobs_station[0]).\
                    order_by(Measurement.date.desc()).first()

#using a datetime class method we can transform our date string into a date object which allows us to better manipulate dates values
# without being forced to hard-code 
mobs_latest_date_obj = dt.date.fromisoformat(mobs_latest_date[0])

#use timedelta method plus operations to create a date object referencing a year from latest date
yrfrm_latest_mobs_date = mobs_latest_date_obj - dt.timedelta(days=365)


"""
This query selects every column within the "measurement table"... where the Measurement.station column matches 
the string representation of our station with the most observations (i.e mobs_station([0]))
... this query additionally filters the selected results for Measurement.date values falling between the latest date and
a year prior from the latest date (for the station with the most observations)
"""
mobs_station_yr_range_query = session.query(Measurement).\
               filter(Measurement.station == mobs_station[0]).\
                              filter(Measurement.date.between(str(yrfrm_latest_mobs_date), str(mobs_latest_date_obj)))



mobs_station_df = pd.read_sql(mobs_station_yr_range_query.statement, engine)
mobs_station_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>station</th>
      <th>date</th>
      <th>prcp</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>14603</td>
      <td>USC00519281</td>
      <td>2016-08-18</td>
      <td>0.00</td>
      <td>80.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>14604</td>
      <td>USC00519281</td>
      <td>2016-08-19</td>
      <td>0.31</td>
      <td>79.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>14605</td>
      <td>USC00519281</td>
      <td>2016-08-20</td>
      <td>0.13</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>14606</td>
      <td>USC00519281</td>
      <td>2016-08-21</td>
      <td>0.08</td>
      <td>79.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>14607</td>
      <td>USC00519281</td>
      <td>2016-08-22</td>
      <td>2.32</td>
      <td>78.0</td>
    </tr>
  </tbody>
</table>
</div>




```python

```


```python
# plot the results as a histogram
mobs_station_df.hist(column= 'tobs', bins=12, grid=True, label="tobs")
plt.ylabel('Frequency')
plt.title('')
plt.legend(loc="best")
```




    <matplotlib.legend.Legend at 0x21dd84baf60>




![png](output_30_1.png)



```python

```


```python
# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
print(calc_temps('2012-02-28', '2012-03-05'))
```

    [(62.0, 69.57142857142857, 74.0)]
    


```python

```


```python
# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.

""" TRIP DATA:
Provided I have a trip start date of "2017-01-01" and an end date of "2017-01-07"
The minimum, average, and maximum temperature would be: """

trip_temps = calc_temps("2017-01-01", "2018-01-09")[0]
trip_temps
```




    (58.0, 74.14387974230493, 87.0)




```python

```


```python
# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)


error = trip_temps[2] - trip_temps[0]

plt.figure(figsize=(1.5,6))
plt.bar(x=[''], height=trip_temps[1], width=0.8,color="salmon", alpha=0.50)
plt.errorbar(x=[''], y=trip_temps[1], yerr=error, elinewidth=1.8, ecolor="black")
plt.yticks([0, 20, 40, 60, 80, 100])

plt.ylim(-5, 110)
plt.ylabel('Temp (F)')
plt.title('Trip Avg Temp')

plt.show()
```


![png](output_36_0.png)



```python

```


```python
# Calculate the rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation


""" 
Provided I have a trip start date of "2017-01-01" and an end date of "2017-01-07"
The amount of rainfall(precipitation) per station would be: 
"""

# This query displays stations and sum of precipitation from each station
"""
To do this, this query selects Measurement.station and func.sum(Measurement.prcp) from the "measurement" table ...
where Measurement.date values fall between the start and end date for my trip...
this query additionally groups the results by station
then orders the groupings by precipitation summation values in descending order.
"""

session.query(Measurement.station, func.sum(Measurement.prcp)).\
        filter(Measurement.date >= "2017-01-01").filter(Measurement.date <= "2017-01-07").\
               group_by(Measurement.station).\
                       order_by(func.sum(Measurement.prcp).desc()).all()
```




    [('USC00519523', 0.61),
     ('USC00514830', 0.6),
     ('USC00516128', 0.6),
     ('USC00513117', 0.35),
     ('USC00519281', 0.2),
     ('USC00519397', 0.0)]




```python

```

## Optional Challenge Assignment


```python
# Create a query that will calculate the daily normals 
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    
daily_normals("01-01")
```




    [(62.0, 69.15384615384616, 77.0)]




```python

```


```python
# Set the start and end date of the trip
start = "2017-01-01"
end = "2017-01-07"

# Use the start and end date to create unique range of dates

# Typecast a numpy range of dates into a list of numpy datetimes
# Note we set the end of the range to one day further than our end date... 
# because the upperbound of numpy arange is not included
np_dates = list(np.arange(start, '2017-01-08', dtype='datetime64[D]'))

# using np.datetime_as_string method, convert list of numpy datetimes into a list of date strings
uniq_date_lst = list(np.datetime_as_string(np_dates))

# Stip off the year and save a list of %m-%d strings:

# select parsed dates from the date column based on dates falling between our start and end dates
date_partial = session.query(func.strftime("%m-%d", Measurement.date)).filter(Measurement.date.between(start, end)).all()

# Create a unique list of partial dates 
"""
Using this unique list of partial dates allows us to acquire a unique collection of normals for each %m-%d (month - day)
"""
uniq_date_prts = []
for date in date_partial:
    if date[0] not in uniq_date_prts:
        uniq_date_prts.append(date[0])
    

# Loop through the list of %m-%d strings and calculate the normals for each date
normals = []
for date in uniq_date_prts:
    normals.append(daily_normals(date)[0])

normals
```




    [(62.0, 69.15384615384616, 77.0),
     (60.0, 69.39622641509433, 77.0),
     (62.0, 68.9090909090909, 77.0),
     (58.0, 70.0, 76.0),
     (56.0, 67.96428571428571, 76.0),
     (61.0, 68.96491228070175, 76.0),
     (57.0, 68.54385964912281, 76.0)]




```python

```


```python
# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index

""" 
Designed a query that builds on the "return" of the daily_normals function

Note:
This query selects the minimum, average, and maximum temperature observations from the Measurement table...
where the month and date ("%m-%d") portion of the strings contained within the Measurement.date column match strings
contained within our uniq_dates list ...
This query then groups the resulting aggregate results by month and date ("%m-%d" )
This essentially gives you rows which correspond to results for every unique date value passed into the daily_normals function


"""



sel2 = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

# Note: "*sel2" <----- this notation allows you to reference every element of a list
daily_normal_query = session.query(*sel2).filter(func.strftime("%m-%d", Measurement.date).in_(uniq_date_prts)).\
             group_by(func.strftime("%m-%d", Measurement.date))

#create a daily normal dataframe using pandas read_sql()
daily_normal_df = pd.read_sql(daily_normal_query.statement, engine, index_col='date')

daily_normal_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>min_1</th>
      <th>avg_1</th>
      <th>max_1</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2011-01-01</th>
      <td>62.0</td>
      <td>69.153846</td>
      <td>77.0</td>
    </tr>
    <tr>
      <th>2014-01-02</th>
      <td>60.0</td>
      <td>69.396226</td>
      <td>77.0</td>
    </tr>
    <tr>
      <th>2010-01-03</th>
      <td>62.0</td>
      <td>68.909091</td>
      <td>77.0</td>
    </tr>
    <tr>
      <th>2010-01-04</th>
      <td>58.0</td>
      <td>70.000000</td>
      <td>76.0</td>
    </tr>
    <tr>
      <th>2010-01-05</th>
      <td>56.0</td>
      <td>67.964286</td>
      <td>76.0</td>
    </tr>
    <tr>
      <th>2010-01-06</th>
      <td>61.0</td>
      <td>68.964912</td>
      <td>76.0</td>
    </tr>
    <tr>
      <th>2016-01-07</th>
      <td>57.0</td>
      <td>68.543860</td>
      <td>76.0</td>
    </tr>
  </tbody>
</table>
</div>




```python

```


```python
# Plot the daily normals as an area plot with `stacked=False`
x = uniq_date_lst
plt.plot(x, daily_normal_df['min_1'], lw=3, alpha=0.4, label= '')
plt.plot(x, daily_normal_df['avg_1'], lw=3, alpha=0.4, label= '')
plt.plot(x, daily_normal_df['max_1'], lw=3, alpha=0.4, label= '')

plt.fill_between(x, daily_normal_df['min_1'], alpha=0.2, label='tmin')
plt.fill_between(x, daily_normal_df['avg_1'], alpha=0.2, label='tavg')
plt.fill_between(x, daily_normal_df['max_1'], alpha=0.2, label='tmax')

plt.xticks(rotation=45)
plt.yticks([0, 20, 40, 60, 80])
plt.xlabel('date')
plt.legend(loc="best")
```




    <matplotlib.legend.Legend at 0x21dd89393c8>




![png](output_47_1.png)



```python

```
