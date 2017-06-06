import requests
import pytest
import time
from multiprocessing import Process


from app.core import main


@pytest.fixture
def app():
    p = Process(target=main)
    p.start()
    time.sleep(4)
    yield True
    p.terminate()
    p.join()



def test_http_echo(app):
    response = requests.get('http://localhost:8080/echo')
    assert response.status_code == 200
    body = response.json()
    assert body.get('foo').get('id') == 25
    assert body.get('foo').get('bar') == 'baz'

def test_http_put(app):
    response = requests.get('http://localhost:8080/echo')
    assert response.status_code == 200
    body = response.json()
    assert body.get('foo').get('id') == 25
    assert body.get('foo').get('bar') == 'baz'



