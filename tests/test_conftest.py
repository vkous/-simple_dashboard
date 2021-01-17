import os
import tempfile
import pytest
import sys
import tests


from dashboard import create_app
from dashboard.model.db import init_db

from flask import url_for

from dotenv import load_dotenv
load_dotenv()
import dashboard.config

app = create_app()

@pytest.fixture # = simple interface to the application
def client():
    with app.test_client() as client:
        #with app.app_context():
        yield client


def test_index_view(client):
    response = client.get('/')
    assert response.status_code == 200


def test_first_visit_default_position(client):
    response = client.get('/')
    with client.session_transaction() as sess:
        latitude = sess['latitude']
        longitude = sess['longitude']
    
    assert (latitude == os.getenv('HOME_LATITUDE'))\
    & (longitude == os.getenv('HOME_LONGITUDE'))

def test_setting_office_position(client):
    response = client.get('/?set_office=')
    with client.session_transaction() as sess:
        latitude = sess['latitude']
        longitude = sess['longitude']
    
    assert (latitude == os.getenv('OFFICE_LATITUDE'))\
    & (longitude == os.getenv('OFFICE_LONGITUDE'))


def test_setting_home_position(client):
    response = client.get('/?set_home=')
    with client.session_transaction() as sess:
        latitude = sess['latitude']
        longitude = sess['longitude']
    
    assert (latitude == os.getenv('HOME_LATITUDE'))\
    & (longitude == os.getenv('HOME_LONGITUDE'))


def test_weather_view(client):
    response = client.get('/view_weather')
    assert response.status_code == 200
    assert (b'Min' in response.data)\
        & (b'Max' in response.data)\
        & (b'Pluie' in response.data)


def test_metro_view(client):
    response = client.get('/view_metro')
    assert response.status_code == 200
    assert b'Ligne' in response.data


def test_bikes_view(client):
    response = client.get('/view_bikes')
    assert response.status_code == 200
    assert b'Station' in response.data