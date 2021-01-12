from .constants import MAPPING_WEATHER_ICONS

from flask import request, redirect, session, url_for

import re

def replace_latitude_longitude(to_replace_string, latitude, longitude):
    return str(to_replace_string).replace('__LONGITUDE__',str(longitude)).replace('__LATITUDE__',str(latitude))


def map_weather_icons_to_forecast(weather_pdf):
    local_df = weather_pdf.copy()
    local_df.loc[:,'icon'] = local_df.loc[:,'weather'].map(MAPPING_WEATHER_ICONS)
    return local_df

def replace_svg_file_by_html_code(html_string):
    regex_string = '<td>([a-z]*).svg</td>'
    return re.sub(
        regex_string,
        '<td><img src="' + url_for('static',filename='icons/') + \
        '\\1.svg" class="icon" style="width:50px" /></td>',
        html_string
        )

def isnumber(number, logger_name = '', attribute='attribute'):
    if isinstance(number, numbers.Number):
        return True
    else:
        current_app.logger.info(
            f'{logger_name} | Error updating {attribute} : not a number')
        return False

def replace_svg_and_translate(html_string):
    return replace_svg_file_by_html_code(translate_weekdays_to_french(html_string))

def translate_weekdays_to_french(html_or_string):
    return html_or_string\
                .replace('Monday','Lundi')\
                .replace('Tuesday','Mardi')\
                .replace('Wednesday','Mercredi')\
                .replace('Thursday','Jeudi')\
                .replace('Friday','Vendredi')\
                .replace('Saturday','Samedi')\
                .replace('Sunday','Dimanche')


def build_collapse_html_block(html, id_name, collapse_text):
    return  f'<br />\
        <p><a class="btn btn-primary" data-toggle="collapse" href="#Collapse{id_name}"\
         role="button" aria-expanded="false" aria-controls="CollapseMaison">{collapse_text}</a></p>\
          <div class="collapse multi-collapse" id="Collapse{id_name}">{html}\
    </div>'


def weather_and_rain_to_html(weather_dict, rain_dict):
    _hourly_pdf = weather_dict['hourly']
    _daily_pdf = weather_dict['daily']
    _rain_next_hour = rain_dict['next_hour']
    _rain_next_12_hours = rain_dict['next_12_hours']

    _rain_html = '<div class="rain"><p>'
    if _rain_next_hour == 0:
        if _rain_next_12_hours == 0 :
            _rain_html += "Pas de pluie dans les 12 prochaines heures"
        else:
            _rain_html += f"Pas de pluie dans l'heure.<br />\
                        Pluie dans les 12 prochaines heures {_rain_next_12_hours} mm"
    else:
        _rain_html += f"Pluie dans l'heure : {_rain_next_hour} mm. <br />\
                    Pluie dans les 12 prochaines heures : {_rain_next_12_hours} mm"
    _rain_html += '</p></div>'
    _weather_table_html = (
        _rain_html + \
        _hourly_pdf.to_html(
            classes=['weather_hourly','table','table-bordered','table-responsive','table-hover'],
            index=False,
            justify="left") + '<!--Beginnning collapse block-->' + \
        build_collapse_html_block(
            html = _daily_pdf.to_html(
                classes=['weather_daily','table','table-bordered','table-responsive','table-hover'],
                index=False,
                justify="left"),
            id_name='daily_weather',
            collapse_text="Prévisions jours suivants"
        )
    ) + '<!-- End weather html table-->'
    return replace_svg_and_translate(_weather_table_html)
