## Advanced-Data-Storage-and-Retrieval-

# Background:
Climate Analysis of a climate database that utilizes completed SQLAlchemy queries to develop an intuitive Flask API.

## Step 1 - Climate Analysis and Exploration

To begin, I used Python and SQLAlchemy to perform basic climate analysis and data exploration of the provided climate database. All of the following analyses were completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Choose a start date and end date for the trip. Make sure that your vacation range is approximately 3-15 days total.

* Used SQLAlchemy `create_engine` to connect to sqlite database.

* Used SQLAlchemy `automap_base()` to reflect tables into classes and save a reference to those classes called `Station` and `Measurement`.

### Precipitation Analysis

* Designed a query to retrieve the last 12 months of precipitation data.

* Selected only the `date` and `prcp` values.

* Loaded the query results into a Pandas DataFrame and set the index to the date column.

* Sorted the DataFrame values by `date`.

* Plotted the results using the DataFrame `plot` method.


* Use Pandas to print the summary statistics for the precipitation data.

### Station Analysis

* Designed a query to calculate the total number of stations.

* Designed a query to find the most active stations.

  * Listed the stations and observation counts in descending order.

  * Answered: Which station has the highest number of observations? using functions such as `func.min`, `func.max`, `func.avg`, and `func.count`.

* Designed a query to retrieve the last 12 months of temperature observation data (tobs).

  * Filtered by the station with the highest number of observations.

  * Plotted the results as a histogram with `bins=12`.


### Temperature Analysis 

* Used a function called `calc_temps` that will accept a start date and end date in the format `%Y-%m-%d` and return the minimum, average, and maximum temperatures for that range of dates.

* Used the `calc_temps` function to calculate the min, avg, and max temperatures for the trip using the matching dates from the previous year (i.e., use "2017-01-01" if your trip start date was "2018-01-01").

* Plotted the min, avg, and max temperature from your previous query as a bar chart.

  * Used the average temperature as the bar height.

  * Used the peak-to-peak (tmax-tmin) value as the y error bar (yerr).


### Other Analysis 

  * Calculated the rainfall per weather station using the previous year's matching dates.

* Calculated the daily normals. Normals are the averages for the min, avg, and max temperatures.

  * Used a function called `daily_normals` that will calculate the daily normals for a specific date. This date string will be in the format `%m-%d`. Be sure to use all historic tobs that match that date string.

  * Created a list of dates for your trip in the format `%m-%d`. Use the `daily_normals` function to calculate the normals for each date string and append the results to a list.

  * Loaded the list of daily normals into a Pandas DataFrame and set the index equal to the date.

  * Used Pandas to plot an area plot (`stacked=False`) for the daily normals.

- - -

## Step 2 - Climate App

* Use FLASK to create your routes.

### Routes

* `/`

  * Home page.

  * Lists all routes that are available.

* `/api/v1.0/precipitation`

  * Converts the query results to a Dictionary using `date` as the key and `prcp` as the value.

  * Returns the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Returns a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Querys for the dates and temperature observations from a year from the last data point.
  * Returns a JSON list of Temperature Observations (tobs) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive. 

