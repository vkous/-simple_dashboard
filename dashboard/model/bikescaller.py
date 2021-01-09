from .apicaller import APICaller
from .constants import API_VELIB_URL

import pandas as pd
import numpy as np

class BikesCaller(APICaller):
    def __init__(self):
        super().__init__()
        self._logger_name = 'Bikes'
        self._db_tablename = 'bikes' 
        self._data_list = ['velib_status']
        self._key_as_table = False
        self._API_base_url = API_VELIB_URL
        self._nb_bikes_int = 10
    
    def _clean_decoded_API_data(self, json_data):
        _bikes_data_pdf = pd.json_normalize(json_data['records'])
        #_bike_data_pdf.drop(['fields.coordonnees_geo'], axis=1, inplace=True)
        _bikes_columns_list = ['fields.capacity',
                            'fields.name',
                            'fields.numbikesavailable',
                            'fields.mechanical',
                            'fields.ebike']

        _bikes_columns_renamed_list = ['capacity',
                                    'bikes_name',
                                    'numbikesavailable',
                                    'mechanical',
                                    'ebike']

        _bikes_data_pdf = _bikes_data_pdf[_bikes_columns_list]
        _bikes_data_pdf.columns = _bikes_columns_renamed_list
        _bikes_data_pdf.loc[:,'taux_remplissage'] = np.round(
            _bikes_data_pdf['numbikesavailable'].divide(_bikes_data_pdf['capacity'])*100,0
            ).astype('int32')
        _bikes_data_pdf = _bikes_data_pdf[['bikes_name','mechanical','ebike','taux_remplissage']]
        _bikes_data_pdf = _bikes_data_pdf.sort_values(by='mechanical', ascending=False).head(self._nb_bikes_int)
    
        self.data_dict = {
            'velib_status': _bikes_data_pdf
        }
        return self.data_dict
    

    def prepare_data_for_html(self):
        _bikes_data_pdf = self.data_dict['velib_status']
        _bikes_data_pdf = _bikes_data_pdf[['bikes_name','mechanical','ebike','taux_remplissage']]
        _bikes_data_pdf.columns = ['Station','Méca','Elec','% Rempl.']
    
        return {
            'velib_status': _bikes_data_pdf
        }
    

    def to_html(self):
        _bikes_data_pdf = self.prepare_data_for_html()['velib_status']
        return {'velib_status' : _bikes_data_pdf.to_html(
            classes=['bikes','table','table-bordered','table-responsive','table-hover'],
            index=False,
            justify="left"
        )}
        