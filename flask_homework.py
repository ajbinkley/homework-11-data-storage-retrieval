import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
from datetime import datetime
from datetime import timedelta as td

from flask import Flask, jsonify

year_start = dt.date(2016, 8, 23)
year_end = dt.date(2017, 8, 23)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to each table
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


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page ya bish!"


# 4. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def tobs_last_year():
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= year_start).\
    filter(Measurement.date <= year_end).\
    all()
    
    dict_convert = {i[0] : i[1] for i in results}
    
    
    return jsonify(dict_convert)
    

    
# 5. Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def station_list():
    stations = session.query(Measurement.station).\
    group_by(Measurement.station).\
    all()
    
    stations_list = list(np.ravel(stations))   
    
    return jsonify(stations_list)
    

    
    
# 6. Define what to do when a user hits the /tobs route
@app.route("/api/v1.0/tobs")
def tobs_list():
    tobs = session.query(Measurement.tobs).\
    filter(Measurement.date >= year_start).\
    filter(Measurement.date <= year_end).\
    all()
    
    tobs_list = list(np.ravel(tobs))   
    
    return jsonify(tobs_list)    
    
 
    
    
# 7. Define what to do when a user hits the <start>/<end> route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    start_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).\
    all()

    start_end_list = list(np.ravel(start_end))   

    return jsonify(start_end_list)             

if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    