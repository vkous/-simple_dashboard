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


from .model import db, metro, bikes, weather, utils, rain

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

    

@app.route('/view_weather', methods=['GET'])
def view_weather():
    #force update
    if session.get('delta_mins') is None:
        session['delta_mins'] = 15
    if request.args.get('update') is not None:
        return utils.force_update()
    
    #get data
    weather_daily_pdf_dict = weather.check_and_update_weather_db(
        latitude = session['latitude'],
        longitude = session['longitude'],
        delta_mins = session['delta_mins'])
    rain_pdf = rain.check_and_update_rain_db(
        latitude = session['latitude'],
        longitude = session['longitude'],
        delta_mins = session['delta_mins'])
    print(rain_pdf)
    
    #reset forced update data when data is got
    session['delta_mins'] = 15

    #prepare html
    update_time_string = pd.to_datetime(weather_daily_pdf_dict['daily']['weather_date']\
        .head(1).values[0]).strftime('%d/%m à %H:%M')
    
    weather_daily_pdf_dict['daily'] = weather_daily_pdf_dict['daily'][['weather_weekday','temp_min','temp_max','icon']]
    weather_daily_pdf_dict['daily'].columns = ['Jour','Min','Max','Météo']
    weather_daily_pdf_dict['hourly'] = weather_daily_pdf_dict['hourly'][['hour','temp','icon']]
    weather_daily_pdf_dict['hourly'].columns = [['Heure','Température','Météo']]
    rain_next_hour = rain_pdf['next_hour'].head(1).values[0]
    rain_next_12_hours = rain_pdf['next_12_hours'].head(1).values[0]
    rain_html = '<div class="rain"><p>'
    if rain_next_hour == 0:
        if rain_next_12_hours == 0:
            rain_html += "Pas de pluie dans les 12 prochaines heures"
        else:
            rain_html += f"Pas de pluie dans l'heure.<br />\
                        Pluie dans les 12 prochaines heures {rain_next_12_hours} mm"
    else:
        rain_html += f"Pluie dans l'heure : {rain_next_hour} mm. <br />\
                    Pluie dans les 12 prochaines heures : {rain_next_12_hours} mm"
    rain_html += '</p></div>'
    weather_table_html = (
        rain_html + \
        weather_daily_pdf_dict['hourly'].to_html(
            classes=['weather_hourly','table','table-bordered','table-responsive','table-hover'],
            index=False,
            justify="left") + '<!--Beginnning collapse block-->' + \
        utils.build_collapse_html_block(
            html = weather_daily_pdf_dict['daily'].to_html(
                classes=['weather_daily','table','table-bordered','table-responsive','table-hover'],
                index=False,
                justify="left"),
            id_name='daily_weather',
            collapse_text="Prévisions jours suivants"
        )
    ) + '<!-- End weather html table-->'
    weather_table_html = weather.replace_svg_and_translate(weather_table_html)

    return render_template(
        'dashboard.html',
        last_update_weather=update_time_string,
        weather_table_html=weather_table_html,
        latitude=session['latitude'],
        longitude=session['longitude']
        )

@app.route('/view_bikes', methods=['GET'])
def view_bikes():
    if session.get('delta_mins') is None:
        session['delta_mins'] = 15
    if request.args.get('update') is not None:
        return utils.force_update() #delta_mins = 1 et redirection vers page précédente
    
    app.logger.info(f"latitude:{session['latitude']}")
    app.logger.info(f"longitude:{session['longitude']}")
    app.logger.info(f"delta_mins:{session['delta_mins']}")
    bikes_pdf = bikes.check_and_update_bike_db(
        latitude=session['latitude'],
        longitude=session['longitude'],
        delta_mins=session['delta_mins']
        )
    session['delta_mins'] = 15
    update_time_string = pd.to_datetime(bikes_pdf['bikes_date'].head(1).values[0]).strftime('%d/%m à %H:%M')
    bikes_pdf = bikes_pdf[['bikes_name','mechanical','ebike','taux_remplissage']]
    bikes_pdf.columns = ['Station','Méca','Elec','% Rempl.']
    bikes_table_html = bikes_pdf\
        .to_html(
            classes=['bikes','table','table-bordered','table-responsive','table-hover'],
            index=False,
            justify="left"
        )
    return render_template(
        'dashboard.html',
        last_update_bikes=update_time_string,
        bikes_table_html= bikes_table_html,
        latitude=session['latitude'],
        longitude=session['longitude']
        )

@app.route('/view_metro', methods=['GET'])
def view_metro():
    get_lines = request.args.get('lines') # TODO : intégrer fonctionnalité ajout de lignes
    if get_lines is None : 
        lines = json.loads(os.getenv('METRO_LINES'))
    else:
        print('yet unimplemented function')
        lines = get_lines
    
    if session.get('delta_mins') is None:
        session['delta_mins'] = 15
    if request.args.get('update') is not None:
        return utils.force_update()

    metro_anormal_pdf = metro.fetch_metro_data_and_get_anormal_status_line(lines)
    #metro.save_metro_to_db(metro_anormal_pdf)
    metro_pdf = metro.check_and_update_date_metro_db(lines = lines, delta_mins=session['delta_mins'])
    session['delta_mins'] = 15

    update_time_string = pd.to_datetime(metro_pdf['metro_date'].head(1).values[0]).strftime('%d/%m à %H:%M')
    metro_table_html = metro_pdf[['metro_line','metro_message']]\
                .to_html(
                    classes=['metro','table','table-bordered', 'table-responsive' 'table-hover'],
                    index=False,
                    justify='left')\
                .replace('metro_line','Ligne')\
                .replace('metro_message','Message')
    
    return render_template(
        'dashboard.html',
        last_update_metro = update_time_string,
        metro_table_html = metro_table_html,
        latitude=session['latitude'],
        longitude=session['longitude']
        )

@app.route('/update_position', methods=['GET','POST'])
def update_position():
    # TODO update position
    #check if post : 
    # si oui : update position via redirect vers / avec mise à jour position
    #sinon 
        # affichage formulaire
    
    return render_template(
        'update_position.html',
        latitude=session['latitude'],
        longitude=str(session['longitude']) + ' - position actuelle'
    )