#Code works for opening website, Can open one API and when trying to open another the site crashes due to an error. Restart the code allows me to open one API
# Either precipitation or station 
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

@app.route("/")
def intro():
    "All APIs"
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")  
    
@app.route("/api/v1.0/precipitation")    
def precipitation():
    recent_year = dt.date(2017,8,23) - dt.timedelta(days = 365)
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > recent_year).order_by(Measurement.date).all()
    # prcp_dict = {}
    # for result in prcp_data:
    #   prcp_dict[precipitation[0]] = precipitation[1]
    prcp_data = []
    for i in precipitation:
        data = {}
        data['date'] = precipitation[0]
        data['prcp'] = precipitation[1]
        prcp_data.append(data)
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def station():
    station_data = session.query(Station.station).all()
    all_station = list(np.ravel(station_data))
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    tobs_list = []
    for i in tobs:
        dict = {}
        dict["station"] = tobs[0]
        dict["tobs"] = float(tobs[1])
        list.append(dict)                             
    return jsonify(tobs_list)

# @app.route("/api/v1.0/<start>")
# def temp_start(start):
#     start = dt.strptime('2016-08-23', '%Y-%m-%d').date()
#     start_results = session.query(func.avg(Measurement.tobs),func.max(Measurement.tobs),func.min(Measurement.tobs).filter(Measurement.date >= start)
# start_list = []
# date_dict = {'start_date': start, 'end_date': max_date}
#         start_list.append(date_dict)
#         start_list.append({'Observation': 'TEMPMIN', 'Temperature': temps[0][0]})
#         start_list.append({'Observation': 'TEMPAVG', 'Temperature': temps[0][1]})
#         start_list.append({'Observation': 'TEMPMAX', 'Temperature': temps[0][2]})
# return jsonify(start_list) 
#     start_list = []   
#     for i in start_results:
#         start_dict = {}
#         start_dict["TMIN"] = float(tobs[1])                     
#         start_dict["TMAX"] = float(tobs[0])
#         start_dict["TAVG"] = float(tobs[2])
#         list.append(start_dict)
#     return jsonify(start_list)

# @app.route("/api/v1.0/<start>/<end>")
# def temps_end(start,end):
#     start = dt.strptime('2016-08-23', '%Y-%m-%d').date()                      
#     end = dt.strptime('2017-08-23', '%Y-%m-%d').date()
#     end_results = session.query(func.avg(Measurement.tobs),func.max(Measurement.tobs),func.min(Measurement.tobs).\
#                filter(Measurement.date >= start)                     
#     start_end_tobs_list = []
#     for i in start_end_tobs_list:
#        dict = {}
#        dict["TMIN"] = float(tobs[1])                     
#        dict["TMAX"] = float(tobs[0])
#        dict["TAVG"] = float(tobs[2])
#        start_end_tobs_list.append(dict)
#     return jsonify(start_end_tobs_list)   
                
if __name__ == "__main__":
    app.run(debug = True)   

