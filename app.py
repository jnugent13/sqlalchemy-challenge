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
        f"/api/v1.0/<start>: Input start date (and end date, if applicable) as yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation/")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query precipitation for all dates
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    
    # Return JSON dictionary using date as key and precipitation as value
    precipitation = []
    for date, prcp in results:
        date_prcp = {date: prcp}
        precipitation.append(date_prcp)

    return jsonify(precipitation)


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

@app.route("/api/v1.0/<start>")
def temp_stats(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query min, avg and max temperatures for date range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    temp_list = []
    for min, max, avg in results:
        temp_stats = {}
        temp_stats['TMIN'] = min
        temp_stats['TAVG'] = avg
        temp_stats['TMAX'] = max
        temp_list.append(temp_stats)
    
    return jsonify(temp_list)


@app.route("/api/v1.0/<start>/<end>")
def temp_list(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query min, avg and max temperatures for date range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    temp_list = []
    for min, max, avg in results:
        temp_stats = {}
        temp_stats['TMIN'] = min
        temp_stats['TAVG'] = avg
        temp_stats['TMAX'] = max
        temp_list.append(temp_stats)
    
    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)
