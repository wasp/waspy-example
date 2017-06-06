from waspy.webtypes import Request, Response


def test_foo_get(transport):
    response = transport.send_request(Request(path='/foo/25'))
    assert response.status.value == 200
    body = response.json()
    assert body.get('foo').get('id') == 25
    assert body.get('foo').get('bar') == 'baz'


def test_foo_put(transport):
    response = transport.send_request(
        Request(path='/foo/25',
                body={'bar': 'barry'},
                method='PUT'))
    assert response.status.value == 200
    body = response.json()
    assert body.get('foo').get('bar') == 'barry'


def test_foo_post(transport):
    response = transport.send_request(
        Request(path='/foo',
                body={'bar': 'blip', 'something': 'else'},
                method='POST')
    )
    assert response.status.value == 201
    assert response.json().get('foo').get('bar') == 'blip'
    assert response.json().get('foo').get('something') == 'else'


def test_foo_patch(transport):
    response = transport.send_request(
        Request(path='/foo/25',
                body={'bar': 'blip', 'something': 'else'},
                method='PATCH')
    )
    assert response.status.value == 200


def test_foo_delete(transport):
    response = transport.send_request(
        Request(path='/foo/25',
                method='DELETE')
    )
    assert response.status.value == 204
