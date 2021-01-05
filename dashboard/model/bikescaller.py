from .apicaller import APICaller
from .constants import API_VELIB_URL

import pandas as pd

class BikesCaller(APICaller):
    def __init__(self, latitude, longitude, delta_mins):
        super().__init__(latitude, longitude, delta_mins)
        self._logger_name = 'Bikes'
        self._db_tablename = 'bikes' 
        self._data_list = ['velib_status']
        self._key_as_table = False
        self._API_base_url = API_VELIB_URL

    
    def clean_decoded_API_data(self, json_data):
        
        self.data_dict = {
            'velib_status': x
        }
        return self.data_dict
    

    def prepare_data_for_html(self):
        
        return {
            'xvelib_status': y_pdf
        }
    

    def to_html(self):
        return {}
        