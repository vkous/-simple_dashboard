from .apicaller import APICaller
from .constants import API_METRO_URL

import pandas as pd
import json
import os

from datetime import timedelta, datetime

class MetroCaller(APICaller):
    def __init__(self, latitude, longitude, delta_mins):
        super().__init__(latitude, longitude, delta_mins)
        self._logger_name = 'Metro'
        self._db_tablename = 'metro' 
        self._data_list = ['metro_status']
        self._key_as_table = False
        self._sql_where_criteria = 'metro_line in {} '.format(
            tuple(json.loads(os.getenv('METRO_LINES')))
        )
        self._key_as_table = False
        self._API_base_url = API_METRO_URL

    def _get_anormal_status_lines(self, metro_status_pdf):
        _anormal_status_lines_pdf = metro_status_pdf.query('slug != "normal"')
        if _anormal_status_lines_pdf.size > 0:
            return [str(x) for x in _anormal_status_lines_pdf['metro_line'].values]
        else:
            return []


    def _add_additional_data(self):
        for key in self.data_dict.keys():
            self.data_dict[key].loc[:, self._db_tablename + '_date'] \
                = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.data_dict

    def _clean_decoded_API_data(self, json_data):
        _metro_data_pdf = pd.json_normalize(json_data['result']['metros'])
        _metro_data_pdf.columns = ['metro_line','slug','title','metro_message']
        _metro_data_pdf.loc[:,'metro_line'] = _metro_data_pdf.loc[:,'metro_line'].astype('string')
        _lines = json.loads(os.getenv('METRO_LINES'))
        _lines = [str(x) for x in _lines]
        _metro_data_pdf = _metro_data_pdf[_metro_data_pdf['metro_line'].isin(_lines)]

        # old treatment in old metro.py file

        self.data_dict = {
            'metro_status': _metro_data_pdf
        }
        return self.data_dict

    #note : read_db_metro => metro_line 
    

    def prepare_data_for_html(self):
        metro_data_pdf = self.data_dict['metro_status']
        metro_data_reduced_pdf = metro_data_pdf[['metro_line','metro_message']]
        return {
            'metro_status': metro_data_reduced_pdf
        }
    

    def to_html(self):
        prepared_pdf = self.prepare_data_for_html()['metro_status']
        return {
            'metro_status': prepared_pdf.to_html(
                classes=['metro','table','table-bordered', 'table-responsive' 'table-hover'],
                index=False,
                justify='left')\
            .replace('metro_line','Ligne')\
            .replace('metro_message','Message')
        }
        