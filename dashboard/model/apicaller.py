from urllib.request import urlopen
import re
import json
import numbers
import pandas as pd
import numpy as np
from datetime import timedelta, datetime

from flask import current_app, url_for, session

from .utils import replace_latitude_longitude, isnumber
from .db import get_db, query_db


class APICaller:
    def __init__(self, latitude, longitude, delta_mins):
        self.latitude = latitude
        self.longitude = longitude
        self.delta_mins = delta_mins
        self.logger_name = 'Base Data'
        self.db_tablename = 'mytable' #for mytable_daily, use mytableand fill-in key
        self.data_list = ['key1','key2']
        self.API_base_url = 'https://apiurl/'
        self.data_dict = {'data_name':pd.DataFrame({})}
        self.restriction_query_dict = {}
        self.restriction_columns_dict = {}
        self.update_boolean = False


    def update_latitude(self, latitude):
        if isnumber(latitude, self.logger_name, 'latitude'):
            self.latitude = latitude


    def update_longitude(self, longitude):
        if isnumber(longitude, self.logger_name, 'longitude'):
            self.longitude = longitude


    def update_delta_mins(self, delta_mins):
        if isnumber(delta_mins, self.logger_name, 'delta_mins'):
            self.delta_mins = delta_mins

    def update_position_and_update_delay_from_session(self):
        update_latitude(session['latitude'])
        update_longitude(session['longitude'])
        update_delta_mins(session['delta_mins'])

    def load_API(self):
        _API_url = replace_latitude_longitude(
            self.API_base_url, self.latitude, self.longitude
            )
        try:
            _API_call_raw_data = urlopen(_API_url)
            return {'API_loading_status' : True, 'raw_data' : _API_call_raw_data}
        except URLError as e:
            current_app.logger.info(
                f'{self.logger_name} | Error loading API {e}')
            return {'API_loading_status' : False}
        else:
            current_app.logger.info(
                f'{self.logger_name} | Unexpected error loading API')
            return {'API_loading_status' : False}
        
    def decode_API_raw_data(self, API_raw_data):
        _raw_data_decoded = API_raw_data.read().decode('utf-8','replace')
        return json.loads(_raw_data_decoded)

    def clean_decoded_API_data(self, json_data):
        #cleaning

        self.data_dict = {
            'key1': pd.DataFrame(),
            'key2': pd.DataFrame()
        }
        return self.data_dict


    def add_additional_data(self):
        for key in self.data_dict.keys():
            self.data_dict[key].loc[:,'latitude'] = self.latitude
            self.data_dict[key].loc[:,'longitude'] = self.longitude
            self.data_dict[key].loc[:, self.db_tablename + '_data'] \
                = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.data_dict


    def restrict_data(self):
        if self.restriction_query_dict != {}:
            for dict_key, restrict_query in self.restriction_query_dict.items():
                self.data_dict[dict_key] = self.data_dict[dict_key].query(restrict_query)
        if self.restriction_columns_dict != {}:
            for dict_key, columns_list in self.restriction_columns_dict.items():
                self.data_dict[dict_key] = self.data_dict[dict_key][columns_list]
        return self.data_dict


    def load_and_clean_data(self):
        _raw_data_dict = self.load_API()
        if _raw_data_dict['API_loading_status'] is True:
            #TODO : exceptions to capture
            _data_json = self.decode_API_raw_data(_raw_data_dict['raw_data'])
            self.clean_decoded_API_data(_data_json)
            self.add_additional_data()
            self.restrict_data()
            self.update_boolean = True
            return {'load_and_clean_data_status' : True}
        else:
            return {'load_and_clean_data_status' : False}


    def save_last_data(self):
        current_app.logger.info(f'{self.logger_name} | Saving data to db')
        _sql_con = get_db()
        for key, pdf in self.data_dict.items():
            pdf.to_sql(
                name = self.db_tablename + str(key),
                con = _sql_con,
                if_exists='append',
                index=False
            )
        current_app.logger.info(f'{self.logger_name} | Data saved to db')
        return True

    def read_last_data(self, additional_key=''):
         #TODO : rewrite with SQL MAX function after first commit



        #additional_key : e.g. : daily for weather_daily table
        current_app.logger.info(f'{self.logger_name} | Reading last entry in db')
        _sql_con = get_db()

        # GET LAST UPDATE DATE
        if additional_key != '':
            _full_tablename = self.db_tablename + '_' + additional_key
        else:
            _full_tablename = self.db_tablename
        _query_string = (
            f'SELECT {self.db_tablename}_date \
                FROM {_full_tablename} \
                WHERE (latitude={self.latitude} AND longitude = {self.longitude}) \
                ORDER BY {self.db_tablename}_date DESC LIMIT 1')
        _sql_last_data_query = query_db(_query_string)
        _sql_last_date_string = _sql_last_data_query[0][{self.db_tablename + '_date'}]
        # to delete if ahead code works
        #for _sql_last_date in _sql_last_data_query:
        #    _sql_last_date_string = _sql_last_date[{self.db_tablename + '_date'}]
        
        # QUERY DB WITH LAST DATE
        _query_string = f"SELECT * FROM {_full_tablename} \
                        WHERE latitude ={self.latitude} \
                        AND longitude = {self.longitude} \
                        AND {self.db_tablename}_date >= '{_sql_last_date_string}'"
        return pd.read_sql(
            _query_string,
            con=_sql_con
        )


    def check_if_data_in_db(self):
        # note : if several keys in data_list, loads only with the first key
        _full_tablename = self.db_tablename + '_' + self.data_list[0]
        _query_string = (
            f'SELECT {self.db_tablename}_date FROM {_full_tablename} \
                WHERE latitude = {self.latitude} \
                AND longitude = {self.longitude} \
                ORDER BY {self.db_tablename}_date DESC \
                LIMIT 1;'
                )
        _query = query_db(_query_string)
        if _query != []:
            return {'existing_entry_status' : True, 'last_date' : _query[0]}
        else:
            return {'existing_entry_status' : False}

    def read_last_updated_data(self, delta_mins = 0):
        _out_dict = {}
        if delta_mins == 0:
            delta_mins = self.delta_mins
        for key in self.data_list:
            _out_dict[key] = read_last_data(
                delta_mins = delta_mins,
                latitude = self.latitude,
                longitude = self.longitude,
                weather_db_type = key
            )
        return _out_dict


    def update_db_with_new_data(self):
        self.load_and_clean_data()
        if self.update_boolean is True:
            self.save_last_data()
            self.update_boolean = False
            return True
        else:
            #error loading API => read older entry
            self.read_last_updated_data(delta_mins = 10000)
            return False


    def check_and_update_db(self):
        _query_db_last_entry_dict = self.check_if_data_in_db()
        if _query_db_last_entry_dict['existing_entry_status'] is True:
            current_app.logger.info(f'{self.logger_name} | existing entries in db')
            _last_update_date = _query_db_last_entry_tuple[1]
        else:
            current_app.logger.info(f'{self.logger_name} | no existing entries in db')
            _last_update_date = datetime.now() - timedelta(minutes=self.delta_mins + 1)
        #if entry is too old : update db
        if (datetime.now() - _last_update_date) > timedelta(minutes = self.delta_mins):
            current_app.logger.info(f'{self.logger_name} | Updating db')
            self.update_db_with_new_data()
        #else : read_db
        else:
            current_app.logger.info(f'{self.logger_name} | Reading last updated data')
            self.read_last_updated_data()

        

    def print_data(self):
        for key,data_pdf in self.data_dict.items():
            print('\n',key)
            print(data_pdf)

    def data_to_html(self):
        return 'True'

