import pytest
from flask import Flask
from routes.groups import groups_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(groups_bp)
    return app

def test_get_groups(client):
    response = client.get('/groups')
    assert response.status_code == 200
    assert 'groups' in response.json

def test_get_group(client):
    response = client.get('/groups/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_get_group_words(client):
    response = client.get('/groups/1/words')
    assert response.status_code == 200
    assert 'words' in response.json

def test_get_group_words_raw(client):
    response = client.get('/groups/1/words/raw')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_group_study_sessions(client):
    response = client.get('/groups/1/study_sessions')
    assert response.status_code == 200
    assert 'study_sessions' in response.json
