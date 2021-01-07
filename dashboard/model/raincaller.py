from .apicaller import APICaller
from .constants import API_METEOFRANCE_RAIN_URL

import pandas as pd
import numpy as np

class RainCaller(APICaller):
    def __init__(self):
        super().__init__()
        self._logger_name = 'Rain'
        self._db_tablename = 'rain' 
        self._data_list = ['rain']
        self._key_as_table = False
        self._API_base_url = API_METEOFRANCE_RAIN_URL

    
    def _clean_decoded_API_data(self, json_data):
        _rain_pdf = pd.json_normalize(json_data['records'])
        
        #.sort_values(by='fields.forecast')
        _rain_pdf = _rain_pdf[['fields.forecast','fields.total_water_precipitation']]
        _rain_pdf = _rain_pdf.astype({'fields.forecast': 'datetime64'})

        _rain_current_hour = _rain_pdf[
            _rain_pdf['fields.forecast'] < pd.Timestamp.now()
            ].tail(1).values[0][1]\
            + _rain_pdf[
                _rain_pdf['fields.forecast'] > pd.Timestamp.now()].head(1).values[0][1]

        _rain_next_12_hours = _rain_pdf[
            _rain_pdf['fields.forecast'] > pd.Timestamp.now()
            ].head(12).sum(axis=1).sum()

        _rain_current_hour = np.round(_rain_current_hour,1)        
        _rain_next_12_hours = np.round(_rain_next_12_hours,1)

        self.data_dict = {
            'rain' : pd.DataFrame(
                {
                    'next_hour' : [_rain_current_hour],
                    'next_12_hours' : [_rain_next_12_hours]
            })
        }
        return self.data_dict
    

    def prepare_data_for_html(self):
        _rain_next_hour = self.data_dict['rain']['next_hour'].values[0]
        _rain_next_12_hours = self.data_dict['rain']['next_12_hours'].values[0]
        return {
            'next_hour': _rain_next_hour,
            'next_12_hours' : _rain_next_12_hours
        }
    