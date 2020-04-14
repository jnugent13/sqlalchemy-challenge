import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation/<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation/<date>")
def precipitation(date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query precipitation for given date
    results = session.query(Measurement.prcp).filter(Measurement.date == date).all()

    session.close()
    
    prcp = {"precipitation": prcp}

    return jsonify(prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station data including the name, lat, long, and elevation of each station"""
    # Query all stations
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()
    
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    """Return a list of temperatures for all dates in last year of data"""
    # Query temperatures for all dates
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= query_date).all()

    session.close()
    
    # Convert list of tuples into normal list
    all_temps = []
    for date, temp in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temp"] = temp
        all_temps.append(temp_dict)

    return jsonify(all_temps)


if __name__ == '__main__':
    app.run(debug=True)
