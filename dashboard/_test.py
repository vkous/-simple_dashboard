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
from .model.utils import weather_and_rain_to_html

@app.route('/', methods=['GET'])
def index():
    #get latitude & longitude
    if 'lat' in request.args:
        try:
            get_latitude = float(request.args.get('lat'))
        except TypeError:
            return redirect(url_for('index'))
        except ValueError:
            return redirect(url_for('index'))
    if 'lon' in request.args:
        try:
            get_longitude = float(request.args.get('lon'))
        except TypeError:
            return redirect(url_for('index'))
        except ValueError:
            return redirect(url_for('index'))

    if ('lat' in request.args) & ('lon' in request.args):
        #update position to desired position
        session['latitude'] = get_latitude
        session['longitude'] = get_longitude
        return redirect(request.referrer)
    elif 'set_office' in request.args:
        #update position to office position
        session['latitude'] = os.getenv('OFFICE_LATITUDE')
        session['longitude'] = os.getenv('OFFICE_LONGITUDE')
        return redirect(request.referrer)
    elif (not (('latitude' in session) & ('longitude' in session))) | ('set_home' in request.args):
        #set home coordinatess
        session['latitude'] = os.getenv('HOME_LATITUDE')
        session['longitude'] = os.getenv('HOME_LONGITUDE')
        if 'set_home' in request.args:
            return redirect(request.referrer)
    #redirect to last url
    return render_template(
        'dashboard.html',
        basic_content_boolean=True,
        latitude=session['latitude'],
        longitude=session['longitude'])



@app.route('/view_bikes', methods=['GET'])
def view_bikes():
    #TODO : when latitude & longitude are not defined
    #force update
    if session.get('delta_mins') is None:
        session['delta_mins'] = 15
    if request.args.get('update') is not None:
        return utils.force_update()
    return True

    
@app.route('/view_weather', methods=['GET'])
def view_weather():
    #TODO : when latitude & longitude are not defined
    #force update
    if session.get('delta_mins') is None:
        session['delta_mins'] = 15
    if request.args.get('update') is not None:
        return utils.force_update()

    #force update
    if session.get('delta_mins') is None:
        session['delta_mins'] = 15
    if request.args.get('update') is not None:
        return utils.force_update()

    weather = WeatherCaller(
        latitude = session['latitude'],
        longitude = session['longitude'],
        delta_mins = session['delta_mins']
    )
    weather.check_and_update_db()

    rain = RainCaller(
        latitude = session['latitude'],
        longitude = session['longitude'],
        delta_mins = session['delta_mins']
    )
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
    #TODO : when latitude & longitude are not defined
    #force update
    if session.get('delta_mins') is None:
        session['delta_mins'] = 15
    if request.args.get('update') is not None:
        return utils.force_update()

    metro = MetroCaller(
        latitude = session['latitude'],
        longitude = session['longitude'],
        delta_mins = session['delta_mins']
    )
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