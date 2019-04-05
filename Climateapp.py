# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

import numpy as np
import pandas as pd

import datetime as dt

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Design a query to retrieve the last 12 months of precipitation data and plot the results

# Find the last date in the table:
# select the first row from the Measurement.date column (ordered in descending order based on date)
# Note the latest_date variable is currently a tuple with one item (a date string)
latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
earliest_date = session.query(Measurement.date).order_by(Measurement.date.asc()).first()

distinct_years = session.query(Measurement.date).\
        filter(Measurement.date >= earliest_date[0]).filter(Measurement.date <= latest_date[0]).distinct()


"""using a datetime class method we can transform our date string (first element of our latest_date tuple)
into a date object which allows us to better manipulate date values without being forced to hard-code 
"""
latest_date_obj = dt.date.fromisoformat(latest_date[0])

# Calculate the date 1 year ago from the last data point in the database
#use timedelta method perations to create a date object referencing a year from latest date
year_ago_from_latest = latest_date_obj - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
year_range_query = session.query(Measurement.date, Measurement.prcp).\
                              filter(Measurement.date.between(str(year_ago_from_latest), str(latest_date_obj))).all()



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
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



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
distinct_years = session.query(Measurement.date).\
    filter(Measurement.date >= earliest_date[0]).filter(Measurement.date <= latest_date[0]).distinct()
    
distinct_year_list = []
for tup in distinct_years:
    distinct_year_list.append(tup[0])



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation_dict = {}
    for row in year_range_query:
        precipitation_dict[row[0]] = row[1]
    precipitation_dict
    return jsonify(precipitation_dict)

stations_tup_list = session.query(Station.station).all()
@app.route("/api/v1.0/stations")
def stations():
    stations_list = []
    for row in stations_tup_list:
        stations_list.append(row[0])
    return jsonify(stations_list)


year_tobs_query = session.query(Measurement.date, Measurement.tobs).\
                              filter(Measurement.date.between(str(year_ago_from_latest), str(latest_date_obj))).all()
@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(year_tobs_query)


@app.route("/api/v1.0/<start>")
def start(start_date):
    if start_date in distinct_year_list:
        temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
        return jsonify(temp_data)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date, end_date):
    if start_date in distinct_year_list and end_date in distinct_year_list:
        return jsonify(calc_temps( start_date, end_date))

if __name__ == '__main__':
    app.run(debug=True)