from .constants import MAPPING_WEATHER_ICONS

from flask import request, redirect, session

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
                .replace('Tuesday','Mardi')\
                .replace('Wednesday','Mercredi')\
                .replace('Thursday','Jeudi')\
                .replace('Friday','Vendredi')\
                .replace('Saturday','Samedi')\
                .replace('Sunday','Dimanche')


def force_update():
    session['delta_mins'] = 1
    return redirect(request.referrer)



def build_collapse_html_block(html, id_name, collapse_text):
    return  f'<br />\
        <p><a class="btn btn-primary" data-toggle="collapse" href="#Collapse{id_name}"\
         role="button" aria-expanded="false" aria-controls="CollapseMaison">{collapse_text}</a></p>\
          <div class="collapse multi-collapse" id="Collapse{id_name}">{html}\
    </div>'


