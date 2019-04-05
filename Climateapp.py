# Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

import numpy as np
import pandas as pd

import datetime as dt

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#create engine
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

# Find the last date in the table:
# select the first row from the Measurement.date column (ordered in descending order based on date)
# Note the latest_date variable is currently a tuple with one item (a date string)
latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Similarly find the earliest date
earliest_date = session.query(Measurement.date).order_by(Measurement.date.asc()).first()

"""using a datetime class method we can transform our date string (first element of our latest_date tuple)
into a date object which allows us to better manipulate date values without being forced to hard-code 
"""
latest_date_obj = dt.date.fromisoformat(latest_date[0])

# Calculate the date 1 year ago from the last data point in the database
#use timedelta method perations to create a date object referencing a year from latest date
year_ago_from_latest = latest_date_obj - dt.timedelta(days=365)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates

def calc_temps(start_date, end_date):
    """
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d       
    Returns:
        TMIN, TAVE, and TMAX
    """
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()




#--------------------------------
################################
#         FLASK SETUP          #
################################
#-------------------------------

app = Flask(__name__)

#--------------------------------
#         HOME ROUTE:           #
#--------------------------------

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes: <br/>"
        f"------------------------ <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/2017-01-01 <br/>"
        f"/api/v1.0/2017-01-01/2017-08-23 <br/>"
    )




#--------------------------------
#         STATIONS ROUTE:       #
#--------------------------------

# This query creates a list of tuples containing stations from our "stations" table
stations_tup_list = session.query(Station.station).all()

# Create an empty list which will hold stations from our "stations" table. 
stations_list = []

# Use a "for loop" to create a list of station strings
# for each tuple in station_tup_list append the first element (i.e the station string) to our stations_list
for row in stations_tup_list:
    stations_list.append(row[0])

@app.route("/api/v1.0/stations")
def stations():
# Return a jsonified list of stations   
    return jsonify(stations_list)


#--------------------------------
#     PRECIPITATION ROUTE:      #
#--------------------------------

station_pre_dict = {}

#This "for loop" creates key-value pairings of stations and dictionaries ... which themselves containing key - value pairings of 
# dates and precipication values specific to each station

for station in stations_list:
#This query creates a list of tuples containing (<date>, <precipitation value>) for dates within a 
# year prior to the last date data point for a specific station
    query = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date.between(str(year_ago_from_latest), str(latest_date_obj))).\
                     filter(Measurement.station == station).all()

# Create an empty list used to store (date - precipitation value) key-value pairs 
    precipitation_dict = {}

# Use a "for loop" to create key-value pairs based on the first and second items of each element in our list of tuples (query)
    for row in query:
        precipitation_dict[row[0]] = row[1]

# Create a key-value pair for each station and its corresponding precipitation dictionary 
    station_pre_dict[station] = precipitation_dict

@app.route("/api/v1.0/precipitation")
def precipitation():
# Return a jsonified list containing a our nested dictionaries
    return jsonify([station_pre_dict])


#----------------------------------
# TEMPERATURE OBSERVATIONS ROUTE: #
#----------------------------------

# # This query creates a list of tuples containing (<station name>, <date>, <temperature observation>) for dates within a 
# # year prior to last date data point.
# year_tobs_query = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
#                               filter(Measurement.date.between(str(year_ago_from_latest), str(latest_date_obj))).all()
# @app.route("/api/v1.0/tobs")
# def tobs():

# # Return a jsonified list of tuples containing (<station name>, <date>, <temperature observation>) for a year from the last data point
#     return jsonify(year_tobs_query)


temperature_dict = {}
for station in stations_list:
    query = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date.between(str(year_ago_from_latest), str(latest_date_obj))).\
                    filter(Measurement.station == station).all()
    temperature_dict[station] = query

@app.route("/api/v1.0/tobs")
def tobs():

# Return a jsonified list of tuples containing (<station name>, <date>, <temperature observation>) for a year from the last data point
    return jsonify([temperature_dict])



#--------------------------------
#       START DATE ROUTE:       #
#--------------------------------

# This query creates a distinct list of date tuples from our "measurement" table
distinct_dates = session.query(Measurement.date).\
    filter(Measurement.date >= earliest_date[0]).filter(Measurement.date <= latest_date[0]).distinct()

# Create an empty list that will hold date strings 
distinct_dates_list = []

# Use a "for loop" to create a list of unique date strings
# for each tuple in distinct_dates append the first element (i.e the date string) to our distinct_dates_list
for tup in distinct_dates:
    distinct_dates_list.append(tup[0])

# @app.route("/api/v1.0/<start>")
# def start(start):
#     if start in distinct_dates_list:
#         temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start).all()
#         return jsonify(temp_data)

def tester(st):
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= st).all()
    return temp_data

@app.route("/api/v1.0/<start>")
def start(start):
    return jsonify(tester(start))

#--------------------------------
#   (START to END) DATE ROUTE:  #
#--------------------------------

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    if start in distinct_dates_list and end in distinct_dates_list:
        return jsonify(calc_temps( start, end))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)