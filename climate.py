#Import of Dependencys
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# Database Setup
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
# Flask Setup
app = Flask(__name__)
# Flask Routes
#   * Home page.
#   * List all routes that are available.
@app.route("/")
def route_avalible():
   """List all available api routes."""
   return (
       f"Available Routes:<br/>"
       f"/api/v1.0/precipitation<br/>"
       f"/api/v1.0/stations"
       f"/api/v1.0/tobs"
       f"/api/v1.0/<start>"
       f"/api/v1.0/<start>/<end>"
   )
# * /api/v1.0/precipitation
#   * Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
   """Return a Json of Precipitation Dates and actual precipitation"""
   # Convert the query results to a Dictionary using date as the key and prcp as the value.
   results = session.query(Measurement.date, Measurement.prcp).all()
   # Return the JSON representation of your dictionary.
   all_precipitation = []
   for date, prcp in results:
       precipitation_dict = {}
       precipitation_dict["date"] = date
       precipitation_dict["prcp"] = prcp
       all_precipitation.append(precipitation_dict)
   return jsonify(all_precipitation)
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""

    print("Received station api request.")

    #query stations list
    stations_data = session.query(Station).all()

    #create a list of dictionaries
    stations_list = []
    for station in stations_data:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        stations_list.append(station_dict)

    return jsonify(stations_list)
   @app.route("/api/v1.0/<start>")
   def start(start):
       """Return a JSON list of the minimum, average, and maximum temperatures from the start date until
       the end of the database."""
   
       print("Received start date api request.")
   
       #First we find the last date in the database
       final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
       max_date = final_date_query[0][0]
   
       #get the temperatures
       temps = calc_temps(start, max_date)
   
       #create a list
       return_list = []
       date_dict = {'start_date': start, 'end_date': max_date}
       return_list.append(date_dict)
       return_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
       return_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
       return_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})
       return jsonify(return_list)
      @app.route("/api/v1.0/<start>/<end>")
      def start_end(start, end):
          """Return a JSON list of the minimum, average, and maximum temperatures from the start date unitl
          the end date."""
      
          print("Received start date and end date api request.")
      
          #get the temperatures
          temps = calc_temps(start, end)
      
          #create a list
          return_list = []
          date_dict = {'start_date': start, 'end_date': end}
          return_list.append(date_dict)
          return_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
          return_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
          return_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})
      
          return jsonify(return_list)
      
      #code to actually run
      if __name__ == "__main__":
          app.run(debug = True)
