from .apicaller import APICaller
from .constants import API_VELIB_URL

import pandas as pd

class RainCaller(APICaller):
    def __init__(self, latitude, longitude, delta_mins):
        super().__init__(latitude, longitude, delta_mins)
        self.logger_name = 'Bikes'
        self.db_tablename = 'bikes' 
        self.data_list = ['velib_status']
        self.key_as_table = False
        self.API_base_url = API_VELIB_URL

    
    def clean_decoded_API_data(self, json_data):

        self.data_dict = {
            'velib_status': x
        }
        return self.data_dict
    

    def prepare_data_for_html(self):
        
        return {
            'xvelib_status': y
        }
    