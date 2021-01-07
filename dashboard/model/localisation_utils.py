from flask import(
    current_app,
    request,
    url_for,
    redirect,
    render_template,
    session,
    g
)

import os
import json

from .flask_utils import redirect_to_last_page, return_template_index_page


def _get_latitude_request_arg():
    if 'lat' in request.args:
        try:
            return (True, float(request.args.get('lat')))
        except TypeError:
            return (False, redirect(url_for('index')))
        except ValueError:
            return (False, redirect(url_for('index')))
    else:
        return (True,None)

def _get_longitude_request_arg():
    if 'lon' in request.args:
        try:
            return (True, float(request.args.get('lon')))
        except TypeError:
            return (False, redirect(url_for('index')))
        except ValueError:
            return (False, redirect(url_for('index')))
    else:
        return(True,None)

def _get_position_request_args():
    lat_tuple = _get_latitude_request_arg()
    lon_tuple = _get_longitude_request_arg()
    print(lat_tuple, lon_tuple)
    if lat_tuple[0] is False | lon_tuple[0] is False:
        return (False, )
    elif (lat_tuple[1] is None) | (lon_tuple[1] is None):
        return (False, )
    else:
        return (True, (lat_tuple[1], lon_tuple[1]))

def _set_latitude_session(latitude):
    session['latitude'] = latitude

def _set_longitude_session(longitude):
    session['longitude'] = longitude

def _set_home_position():
    _set_latitude_session(os.getenv('HOME_LATITUDE'))
    _set_longitude_session(os.getenv('HOME_LONGITUDE'))

def _set_office_position():
    _set_latitude_session(os.getenv('OFFICE_LATITUDE'))
    _set_longitude_session(os.getenv('OFFICE_LONGITUDE'))




def check_default_position():
    if (session['latitude'] is None) | (session['longitude'] is None):
        _set_home_position()

def get_index_or_get_and_set_latitude_and_longitude():
    print(request.referrer)
    position_got_tuple = _get_position_request_args()
    if (position_got_tuple[0] is True) :
        #update position to desired position
        latitude = position_got_tuple[1][0]
        longitude = position_got_tuple[1][1]
        if (latitude is not None) & (longitude is not None):
            current_app.logger.info(
                f'Position | Update latitude {latitude} and longitude {longitude}')
            _set_latitude_session(latitude)
            _set_longitude_session(longitude)
            return redirect_to_last_page()

    if 'set_office' in request.args:
        #update position to office position
        current_app.logger.info(
            f'Position | Setting office position')
        _set_office_position()
        return redirect_to_last_page()
    elif  'set_home' in request.args:
        #set home coordinates
        current_app.logger.info(
            f'Position | Setting home position')
        _set_home_position()
        if 'set_home' in request.args:
            return redirect_to_last_page()
        print('Je suis là')
    print('bizarre')
    return return_template_index_page()
