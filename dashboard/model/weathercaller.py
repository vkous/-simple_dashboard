#import apicaller?
from .constants import API_WEATHER_URL
from .utils import map_weather_icons_to_forecast
from .apicaller import APICaller

import os
import json
import pandas as pd
from datetime import timedelta, datetime

class WeatherCaller(APICaller):
    def __init__(self, latitude, longitude, delta_mins):
        super().__init__(latitude, longitude, delta_mins)
        self.logger_name = 'Weather'
        self.db_tablename = 'weather' 
        self.data_list = ['daily','hourly']
        self.API_base_url = API_WEATHER_URL
        self.restriction_columns_dict={
            'daily': ['weekday', 'day','humidity','wind_speed','temp.min','temp.max','weather'],
            'hourly': ['weekday','hour','humidity','wind_speed','temp','weather']
        }
        

    def clean_decoded_API_data(self, json_data):
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
            _weather_h0_h12_pdf.loc[_watched_hours_list,:].drop('weather',axis=1) # < A REVERIFIER SI ERREUR
        _hourly_weather_pdf.loc[:,'weather'] = _weather_hour_string_list
        _hourly_weather_pdf.loc[:,'weekday'] = 'today'
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
        _daily_weather_pdf.loc[:,'weekday'] = _weather_weekday_string_list
        _daily_weather_pdf.loc[:,'weekday'] = _daily_weather_pdf.loc[:,'weekday'].dt.day_name()
        _daily_weather_pdf.loc[:,'day'] = ['today','J+1','J+2','J+3','J+4','J+5','J+6']
        _daily_weather_pdf = _daily_weather_pdf.query('day != "today"').copy()
        for column in ['humidity','wind_speed','temp.min','temp.max']:
            _daily_weather_pdf.loc[:,column] = _daily_weather_pdf[column].fillna(0).copy().astype('int32')
        _daily_weather_pdf = map_weather_icons_to_forecast(_daily_weather_pdf)

        self.data_dict =  {
            'hourly': _hourly_weather_pdf,
            'daily': _daily_weather_pdf
        }
        return self.data_dict
