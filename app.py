# import dependencies 
import datetime as dt
import numpy as np
import pandas as pd

# import SQL dependencies 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import flask dependencies 
from flask import Flask, jsonify

# access SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes 
Base = automap_base()
Base.prepare(engine, reflect=True)

# creating variable for each class 
Measurement = Base.classes.measurement
Station = Base.classes.station

# creating session link from Python to our database 
session = Session(engine)

# set up Flask 
app = Flask(__name__)

# creating route
#@app.route("/")

#def welcome():
 #   return(
  #  '''
   # Welcome to the Climate Analysis API!
   # Available Routes:
   # /api/v1.0/precipitation
   # /api/v1.0/stations
   # /api/v1.0/tobs
   # /api/v1.0/temp/start/end
   # ''')

# creating route for precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
    
# creating route for station
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# creating route for temperature for previous year 
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= prev_year).all()      
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# creating route for min, max and avg temperature  
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # if not statement to determine end date
    # * shows multiple result for sel (min, max and avg)
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)