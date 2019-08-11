'Author: Rubi Trujillo Godinez'
'Homework number 10  sqlalchemy  - Climate API'

from flask import Flask, jsonify

# import libraries 

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def ini():

    return (
f"<br>"
f"<br>"

f"Hello, Here you can check data regarding the Temprature and precipitacion of Hawaii based on historical records"
f"<br>"
f"<br>"
f"<br>"
f"The available Inquiries you can check are:" 
f"<br>"
f"<br>"
f"<br>"
f"/api/v1.0/precipitation"
f"<br>"
f"<br>"
f"/api/v1.0/stations"
f"<br>"
f"<br>"
f"/api/v1.0/tobs"
f"<br>"
f"<br>"
 )


# PRECIPITATION
@app.route("/api/v1.0/precipitation")
def precipitation():
    # calculate number of months.
    today=(datetime.strptime(str(dt.date.today()), '%Y-%m-%d'))
    twelveago=(datetime.strptime(str(dt.date.today() - dt.timedelta(365*2)), '%Y-%m-%d'))
    twelveago,today
    """Return the precipitation data as json"""
    qry1 = session.query(Measurement.date,Measurement.prcp).\
                filter(Measurement.date > twelveago ).\
                order_by(Measurement.date).all( )
    precip_data = []
    for q in qry1:
        row = {}
        row["date"] = q[0]
        row["prcp"] = q[1]
        precip_data.append(row)

    return jsonify(precip_data)


# Query2&3 Statiosn
@app.route("/api/v1.0/stations")
def station():
    
    """Return the stations data as json"""
    qry4 = session.query(Measurement.station,func.count().label('number')).\
                group_by(Measurement.station).\
                order_by(desc(func.count())).all()
    stations_data = []
    for q in qry4:
        row = {}
        row["station"] = q[0]
        row["number"] = q[1]
        stations_data.append(row)

## pending fixing how to print 
    return jsonify(stations_data)


# Query4 /api/v1.0/tobs   - Temperature observations
@app.route("/api/v1.0/tobs")
def temperature():
    
    """Return the stations data as json"""
    qry5 = session.query(Measurement.station,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                group_by(Measurement.station).\
               order_by(desc(func.count())).all()    
    return jsonify(qry5)




if __name__ == "__main__":
    app.run(debug=True)


