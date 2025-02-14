import pytest
from flask import Flask
from routes.words import load

@pytest.fixture
def app():
    app = Flask(__name__)
    load(app)
    return app

def test_get_words(client):
    response = client.get('/words')
    assert response.status_code == 200
    assert 'words' in response.json

def test_get_word(client):
    response = client.get('/words/1')
    assert response.status_code == 200
    assert 'word' in response.json
