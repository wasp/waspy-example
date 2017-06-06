from waspy.webtypes import Request, Response


def test_echo_call(transport):
    response = transport.send_request(Request(path='/echo'))
    assert response.status.value == 200
    body = response.json()
    assert body.get('headers') == {}
    assert body.get('query') == {}


def test_echo_query_string(transport):
    response = transport.send_request(
        Request(path='/echo', query_string='hello=there&foo=bar'))
    assert response.status.value == 200
    body = response.json()
    assert 'there' in body.get('query').get('hello')
    assert 'bar' in body.get('query').get('foo')


def test_echo_with_multiple_query_of_same_key(transport):
    response = transport.send_request(
        Request(path='/echo', query_string='foo=bar&foo=baz&foo=barry')
    )
    assert response.status.value == 200
    query = response.json().get('query')
    assert 'bar' in query.get('foo')
    assert 'baz' in query.get('foo')
    assert 'barry' in query.get('foo')


def test_post_echo(transport):
    mybody = {'hello': 'world'}
    response = transport.send_request(
        Request(path='/echo', query_string='foo=bar&foo=baz&foo=barry',
                method='POST', body=mybody)
    )
    assert response.status.value == 200
    body = response.json()
    assert body == mybody


def test_put_echo_doesnt_exist(transport):
    response = transport.send_request(
        Request(path='/echo', query_string='foo=bar&foo=baz&foo=barry',
                method='PUT', body={'something': 'here'})
    )
    assert response.status.value == 404


