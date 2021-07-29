#Code works for opening website, and allows for mst route to open except Start/end
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

app = Flask(__name__)

# def calc_temps(start_date, end_date):
#     return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
#Placed into start
def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

@app.route("/")
def main():
    """All APIs"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")  
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    max_date_string = final_date_query[0][0]
    max_date = dt.datetime.strptime(max_date_string, "%Y-%m-%d")

    begin_date = max_date - dt.timedelta(365)

    precipitation_data = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= begin_date).all()
    session.close()

    results_dict = {}
    for result in precipitation_data:
        results_dict[result[0]] = result[1]
    return jsonify(results_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station).all()
    session.close()
    stations_list = []
    for station in stations:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        stations_list.append(station_dict)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    max_date_string = final_date_query[0][0]
    max_date = dt.datetime.strptime(max_date_string, "%Y-%m-%d")
    begin_date = max_date - dt.timedelta(365)
    results = session.query(Measurement).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= begin_date).all()
    session.close()
    
    tobs_list = []
    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result.date
        tobs_dict["station"] = result.station
        tobs_dict["tobs"] = result.tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def data(start=None, end=None):

    if not end: 
        final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
        session.close()
        max_date_string = final_date_query[0][0]
        max_date = dt.datetime.strptime(max_date_string, "%Y-%m-%d")
        start = max_date - dt.timedelta(365)
        temps = calc_temps(start, max_date_string)
        return_list = []
        date_dict = {'start_date': start}
        return_list.append(date_dict)
        return_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
        return_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
        return_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})
        return jsonify(return_list)

def final_calc(start_date, end_date): 
    session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    session.close()
    max_date_string = final_date_query[0][0]
    max_date = dt.datetime.strptime(max_date_string, "%Y-%m-%d")
    start = max_date - dt.timedelta(365)
    temps = final_calc(start, max_date_string)
    end = max_date
    final_list = []
    date_dict = {'start_date': start, 'end_date':end}
    final_list.append(date_dict)
    final_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
    final_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
    final_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})
    return jsonify(final_list)

if __name__ == "__main__":
     app.run(debug=True)   
   
   
   
   
   
#These are codes that I tinkered on for start and start/end
    # final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    # max_date_string = final_date_query[0][0]
    # max_date = dt.datetime.strptime(max_date_string, "%Y-%m-%d")
    # start = max_date - dt.timedelta(365)
    # end = max_date
    # temps = calc_temps(start, max_date_string)
    # SEr_list = []
    # date_dict = {'start_date': start, 'end_date': end}
    # SEr_list.append(date_dict)
    # SEr_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
    # SEr_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
    # SEr_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})
    # return jsonify(SEr_list)  

# @app.route("/api/v1.0/<start>/<end>")
# def start_end(start, end):
#     date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
#     session.close()
#     last_date = date_query[0][0]
#     max_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
#     start = max_date - dt.timedelta(365)
#     temps = calc_temps(start, max_date)
#     end = max_date
#     return_list = []
#     date_dict = {'start_date': start, 'end_date': end}
#     return_list.append(date_dict)
#     return_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
#     return_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
#     return_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})
#     return jsonify(return_list)
# if __name__ == "__main__":
#     app.run(debug=True)

        # start = dt.datetime.strptime(start, "%Y-%m-%d")
        # results = session.query(*calc_temps).\
        #     filter(Measurement.date >= start).all()
        # session.close()
        # start_temps = list(np.ravel(results))