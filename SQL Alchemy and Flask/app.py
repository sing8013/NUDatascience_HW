#import dependencies
import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#connect to hawaii data
engine = create_engine('sqlite:///./Resources/hawaii.sqlite')

Base =  automap_base()
Base.prepare(engine,reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session
session = Session(engine)

# Calculate the date 1 year ago from today
lastyear_date=dt.datetime.today()+relativedelta(years=-2)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f'Welcome to Hawaii \n'
        f'/api/v1.0/precipitation\n'
        f'/api/v1.0/stations\n'
        f'/api/v1.0/tobs \n'
        f'/api/v1.0/<start> - (use mm-dd)' 
        f'/api/v1.0/<start>/<end> (use YYYY-mm-dd)  '
    )

'''* `/api/v1.0/precipitation`
* Query for the dates and temperature observations from the last year.
* Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
* Return the JSON representation of your dictionary.'''
@app.route("/api/v1.0/precipitation")
def precipitation():
    q=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=lastyear_date).all()
    print (q)
    return jsonify(q)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    q = session.query(Station.station,Station.name).all()
    print(q)
    return jsonify(q)

# Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    q = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>=lastyear_date).all()
    print(q)
    return jsonify(q)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def temp1(start):
    date= start #dt.datetime.strptime(start,'%Y-%m-%d')
    sel = [func.min(Measurement.tobs).label('TMIN'), func.avg(Measurement.tobs).label('TAVG'), func.max(Measurement.tobs).label('TMAX')]
    q=session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    print(q)
    return jsonify(q)

#When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def temp2(start,end):
    sel = [func.min(Measurement.tobs).label('TMIN'), func.avg(Measurement.tobs).label('TAVG'), func.max(Measurement.tobs).label('TMAX')]
    q =  session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
        filter(func.strftime("%Y-%m-%d", Measurement.date)  <= end).all()
    print(q)
    return jsonify(q)

if __name__ == "__main__":
    app.run(debug=True)