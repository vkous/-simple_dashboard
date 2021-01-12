from flask import(
    current_app as app,
    request,
    url_for,
    redirect,
    render_template,
    session,
    g
)

import os
import json


def redirect_to_last_page():
    last_page_url = request.referrers
    if (request.referrer.split('?')[0] == url_for('index')) | request.referrer is None :
        return redirect(url_for('index'))
    else:
        return redirect(request.referrer)

def force_update():
    session['delta_mins'] = 1
    return redirect_to_last_page()

def reinitialize_session_delta_mins():
    session['delta_mins'] = 15

def check_delta_mins():
    if session.get('delta_mins') is None:
        reinitialize_session_delta_mins()
    if request.args.get('update') is not None:
        return force_update()

def return_template_index_page():
    if not ('latitude' in session) & ('longitude' in session):
         _latitude = None
         _longitude = None
    else:
        _latitude = session['latitude']
        _longitude = session['longitude']

    return render_template(
        'dashboard.html',
        basic_content_boolean=True,
        latitude = _latitude,
        longitude= _longitude)