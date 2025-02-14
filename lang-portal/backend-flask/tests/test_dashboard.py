import pytest
from flask import Flask
from routes.dashboard import load

@pytest.fixture
def app():
    app = Flask(__name__)
    load(app)
    return app

def test_get_recent_session(client):
    response = client.get('/dashboard/recent-session')
    assert response.status_code == 200

def test_get_study_stats(client):
    response = client.get('/dashboard/stats')
    assert response.status_code == 200
    assert 'total_vocabulary' in response.json
