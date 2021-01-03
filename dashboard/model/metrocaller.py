from .apicaller import APICaller
from .constants import API_METRO_URL

import pandas as pd
import json
import os

class MetroCaller(APICaller):
    def __init__(self, latitude, longitude, delta_mins):
        super().__init__(latitude, longitude, delta_mins)
        self.logger_name = 'Metro'
        self.db_tablename = 'metro' 
        self.data_list = ['metro_status']
        self.sql_where_criteria = 'metro_line in {} '.format(
            tuple(json.loads(os.getenv('METRO_LINES')))
        )
        self.key_as_table = False
        self.API_base_url = API_METRO_URL

    def get_anormal_status_lines(self, metro_status_pdf):
        _anormal_status_lines_pdf = metro_status_pdf.query('slug != "normal"')
        if _anormal_status_lines_pdf.size > 0:
            return [str(x) for x in _anormal_status_lines_pdf['metro_line'].values]
        else:
            return []

    def clean_decoded_API_data(self, json_data):
        _metro_data_pdf = pd.json_normalize(json_data['result']['metros'])
        _metro_data_pdf.columns = ['metro_line','slug','title','metro_message']
        _metro_data_pdf.loc[:,'metro_line'] = _metro_data_pdf.loc[:,'metro_line'].astype('string')
        _lines = json(os.getenv('METRO_LINES'))
        _metro_data_pdf = _metro_data_pdf.query('metro_line == @_lines')

        # old treatment in old metro.py file

        self.data_dict = {
            'metro_status': _metro_data_pdf
        }
        return self.data_dict

    #note : read_db_metro => metro_line 
    

    def prepare_data_for_html(self):
        
        return {
            'metro_status': x
        }
    