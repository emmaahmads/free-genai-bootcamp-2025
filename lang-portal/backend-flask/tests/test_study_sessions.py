import pytest
from flask import Flask
from routes.study_sessions import study_sessions_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(study_sessions_bp)
    return app

def test_create_study_session(client):
    response = client.post('/study_sessions', json={
        'group_id': 1,
        'start_time': '2023-01-01T00:00:00Z',
        'end_time': '2023-01-01T01:00:00Z',
        'score': 100
    })
    assert response.status_code == 201
    assert 'id' in response.json

def test_get_study_sessions(client):
    response = client.get('/api/study-sessions')
    assert response.status_code == 200
    assert 'items' in response.json

def test_get_study_session(client):
    response = client.get('/api/study-sessions/1')
    assert response.status_code == 200
    assert 'session' in response.json

def test_review_study_session(client):
    response = client.post('/study_sessions/1/review', json={
        'review_notes': 'Great session',
        'rating': 5
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Study session reviewed successfully'

def test_reset_study_sessions(client):
    response = client.post('/api/study-sessions/reset')
    assert response.status_code == 200
    assert response.json['message'] == 'Study history cleared successfully'
