import re
from pyramid.url import urlencode


def test_root(testapp):
    res = testapp.get('/', status=200)
    assert b'Cinchworm' in res.body


def test_notfound(testapp):
    res = testapp.get('/badurl', status=404)
    assert res.status_code == 404


def test_convert(testapp):
    filename = 'tests/support/example.bin'
    file = open(filename, 'rb').read()
    data = [('binary_data', filename, file)]
    res = testapp.post('/compress', {}, upload_files=data)
    assert res.status_code == 302
    base_location = res.headers['Location'].split('&')[0]
    assert base_location == f'http://example.com/complete?{urlencode(dict(filename=filename))}'


def test_complete(testapp):
    res = testapp.get('/complete?filename=snorlax.bin', status=200)
    assert b'Original Size' in res.body
    assert b'snorlax.bin' in res.body
