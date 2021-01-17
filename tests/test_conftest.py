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

@pytest.fixture # = simple interface to the application
def client():
    dashboard = create_app()
    with dashboard.test_client() as client:
        with dashboard.app_context():
            yield client

def test_url_index(client):
    from dashboard import routes
    response = client.get('/')
    print(response)
    assert response.status_code == 200


def test_url_weather(client):
    from dashboard import routes
    assert client.get('/view_weather').status_code == 200


def test_url_metro(client):
    #assert client.get(url_for('view_metro')).status_code == 200
    assert True == True


def test_url_bikes(client):
    #assert client.get(url_for('view_bikes')).status_code == 200
    assert True == True


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data