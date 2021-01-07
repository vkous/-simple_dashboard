from .constants import API_WEATHER_URL
from .utils import map_weather_icons_to_forecast
from .apicaller import APICaller

import os
import json
import pandas as pd
from datetime import timedelta, datetime

class WeatherCaller(APICaller):
    def __init__(self):
        super().__init__()
        self._logger_name = 'Weather'
        self._db_tablename = 'weather' 
        self._key_as_table = True
        self._data_list = ['daily','hourly']
        self._API_base_url = API_WEATHER_URL
        self._restriction_columns_dict={
            'daily': ['weather_weekday','weather_day', 'temp_min','temp_max','latitude','longitude','weather_date','icon'],
            'hourly': ['weather_weekday','hour','temp','latitude','longitude','weather_date','icon']
        }

    def _clean_decoded_API_data(self, json_data):
        #Todo : break_up cleaning

        # Clean Hourly Data
        _weather_h0_h12_pdf = pd.json_normalize(json_data['hourly'][0:12])
        _watched_hours_list = json.loads(os.getenv('WEATHER_HOURS'))
        _weather_hour_string_list = []
        _weather_datetime_string_list = []

        for hour in _watched_hours_list:
            _weather_hour_string_list.append(
                _weather_h0_h12_pdf.loc[hour,:]['weather'][0]['description']
            )
            _weather_datetime_string_list.append(
                datetime.fromtimestamp(_weather_h0_h12_pdf.loc[hour,:]['dt']).hour
            )
        _hourly_weather_pdf = \
            _weather_h0_h12_pdf.loc[_watched_hours_list,:].drop('weather',axis=1) # < MAY CAUSE ERROR?
        _hourly_weather_pdf.loc[:,'weather'] = _weather_hour_string_list
        _hourly_weather_pdf.loc[:,'weather_weekday'] = 'today'
        _hourly_weather_pdf.loc[:,'temp'] = _hourly_weather_pdf.loc[:,'temp'].copy().astype('int32')
        _hourly_weather_pdf.loc[:,'hour'] = _weather_datetime_string_list
        _hourly_weather_pdf = map_weather_icons_to_forecast(_hourly_weather_pdf)

        # Clean Daily_data
        _weather_d0_d6_pdf = pd.json_normalize(json_data['daily'][0:7])
        _weather_day_string_list = []
        _weather_weekday_string_list = []
        _today = pd.to_datetime('today').normalize()
        for day in range(0,7):
            _weather_day_string_list.append(
                _weather_d0_d6_pdf['weather'][day][0]['description']
            )
            _weather_weekday_string_list.append(
                _today + timedelta(days = day)
            )
        _daily_weather_pdf = _weather_d0_d6_pdf.drop('weather',axis=1).copy()
        _daily_weather_pdf.loc[:,'weather'] = _weather_day_string_list
        _daily_weather_pdf.loc[:,'weather_weekday'] = _weather_weekday_string_list
        _daily_weather_pdf.loc[:,'weather_weekday'] = _daily_weather_pdf.loc[:,'weather_weekday'].dt.day_name()
        _daily_weather_pdf.loc[:,'weather_day'] = ['today','J+1','J+2','J+3','J+4','J+5','J+6']
        _daily_weather_pdf = _daily_weather_pdf.query('weather_weekday != "today"').copy()
        _daily_weather_pdf.columns = [x.replace('.','_') for x in _daily_weather_pdf.columns]
        for column in ['humidity','wind_speed','temp_min','temp_max']:
            _daily_weather_pdf.loc[:,column] = _daily_weather_pdf[column].fillna(0).copy().astype('int32')
        _daily_weather_pdf = map_weather_icons_to_forecast(_daily_weather_pdf)

        self.data_dict =  {
            'hourly': _hourly_weather_pdf,
            'daily': _daily_weather_pdf
        }
        return self.data_dict

    def prepare_data_for_html(self):
        _daily_pdf = self.data_dict['daily']
        _hourly_pdf = self.data_dict['hourly']
        _update_time_string = pd.to_datetime(_daily_pdf['weather_date']\
            .head(1).values[0]).strftime('%d/%m à %H:%M')

        _daily_pdf = _daily_pdf[['weather_weekday','temp_min','temp_max','icon']]
        _daily_pdf.columns = ['Jour','Min','Max','Météo']
        _daily_pdf.loc[:,'Min'] = _daily_pdf.loc[:,'Min'].apply(str) + '°C'
        _daily_pdf.loc[:,'Max'] = _daily_pdf.loc[:,'Max'].apply(str) + '°C'
        _hourly_pdf = _hourly_pdf[['hour','temp','icon']]
        _hourly_pdf.columns = ['Heure','Température','Météo']
        _hourly_pdf.loc[:,'Heure'] = _hourly_pdf.loc[:,'Heure'].apply(str) + 'H' 
        _hourly_pdf.loc[:,'Température'] = _hourly_pdf.loc[:,'Température'].apply(str) + '°C'
        return {
            'daily' : _daily_pdf,
            'hourly' : _hourly_pdf
            }

    def to_html(self):
        return {}
        
    