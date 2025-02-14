import pytest
from flask import Flask
from routes.study_activities import load

@pytest.fixture
def app():
    app = Flask(__name__)
    load(app)
    return app

def test_get_study_activities(client):
    response = client.get('/api/study-activities')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_study_activity(client):
    response = client.get('/api/study-activities/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_get_study_activity_sessions(client):
    response = client.get('/api/study-activities/1/sessions')
    assert response.status_code == 200
    assert 'items' in response.json

def test_get_study_activity_launch_data(client):
    response = client.get('/api/study-activities/1/launch')
    assert response.status_code == 200
    assert 'activity' in response.json
    assert 'groups' in response.json
