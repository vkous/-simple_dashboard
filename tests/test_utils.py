from dashboard.model.utils import replace_latitude_longitude,translate_weekdays_to_french
from dashboard.model.flask_utils import redirect_to_last_page, force_update
from dashboard.model.localisation_utils import (
    _get_latitude_request_arg,
    _get_longitude_request_arg,
    _get_position_request_args,
    _set_home_position,
    _set_office_position
    )

from dashboard.model.db import get_db, close_db, query_db, change_db

def test_replace_latitude_longitude():
    test_string='abc__LATITUDE__eofeuofeafboea?ZENJOFAENLFEAL__LONGITUDE__eanfeofeaobfeanjoc,nc"à_'
    test_final_string = 'abc2.45843eofeuofeafboea?ZENJOFAENLFEAL48.383eanfeofeaobfeanjoc,nc"à_'
    assert replace_latitude_longitude(test_string, 2.45843, 48.383) == test_final_string
 

def test_translate_weekdays_to_french():
    assert translate_weekdays_to_french('Wednesday') == 'Mercredi'

'''
def test_db():
    assert True == True


def test_redict_to_last_page():
    assert True == True


def test_reject_object_get_latitude_request_args():
    # test 
    assert True == True


def test_reject_object_get_longitude_request_args():
    # test 
    assert True == True


def test_set_home_position():
    assert True == True


def test_set_office_position():
    assert True == True
'''