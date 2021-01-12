from flask import (
    current_app as app,
    request,
    url_for,
    redirect, 
    render_template,
    session,
    g)

import pandas as pd
import os
import json


from .model.weathercaller import WeatherCaller
from .model.raincaller import RainCaller
from .model.metrocaller import MetroCaller
from .model.bikescaller import BikesCaller
from .model.utils import weather_and_rain_to_html
from .model.flask_utils import force_update, check_delta_mins
from .model.localisation_utils import (
    get_index_or_get_and_set_latitude_and_longitude,
    check_default_position)


@app.route('/',methods=['GET'])
def index():
    check_default_position()
    check_delta_mins()
    return get_index_or_get_and_set_latitude_and_longitude()


@app.route('/view_bikes', methods=['GET'])
def view_bikes():
    #TODO : when latitude & longitude are not defined
    check_default_position()
    check_delta_mins()

    bikes = BikesCaller()
    bikes.check_and_update_db()

    return render_template(
        'dashboard.html',
        bikes_table_html=bikes.to_html()['velib_status'],
        last_update_bikes = bikes.last_update,
        latitude = session['latitude'],
        longitude = session['longitude']
    )

    
@app.route('/view_weather', methods=['GET'])
def view_weather():
    #TODO : when latitude & longitude are not defined
    check_default_position()
    check_delta_mins()

    weather = WeatherCaller()
    weather.check_and_update_db()
    rain = RainCaller()
    rain.check_and_update_db()

    weather_html = weather_and_rain_to_html(
        weather.prepare_data_for_html(),
        rain.prepare_data_for_html()
        )
    return render_template(
        'dashboard.html',
        last_update_weather = weather.last_update,
        weather_table_html = weather_html,
        latitude = session['latitude'],
        longitude = session['longitude']
        )
    
@app.route('/view_metro', methods=['GET'])
def view_metro():
    check_default_position()
    check_delta_mins()

    metro = MetroCaller()
    metro.check_and_update_db()
    metro_html = metro.to_html()

    return render_template(
        'dashboard.html',
        last_update_metro = metro.last_update,
        metro_table_html = metro_html['metro_status'],
        latitude = session['latitude'],
        longitude = session['longitude']
    )

@app.route('/update_position', methods=['GET','POST'])
def update_position():
    return render_template(
        'update_position.html',
        latitude=session['latitude'],
        longitude=str(session['longitude']) + ' - position actuelle'
    )