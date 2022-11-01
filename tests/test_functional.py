from curses import meta
import os
import json
from pyramid.url import urlencode


def test_root(testapp):
    res = testapp.get('/', status=200)
    assert b'Cinchworm' in res.body


def test_notfound(testapp):
    res = testapp.get('/badurl', status=404)
    assert res.status_code == 404


def test_compress(testapp):
    # setup for test file upload
    filename = 'tests/support/example.bin'
    with open(filename, 'rb') as rawdata:
        file = rawdata.read()
    data = [('binary_data', filename, file)]

    # POST
    res = testapp.post('/compress', {}, upload_files=data)
    assert res.status_code == 302

    # pull access key from redirect url
    location = res.headers['Location'].split('?')
    base_location = location[0]
    assert base_location == f'http://example.com/complete'
    access_key_id = location[1].split('=')[1]

    # verify metadata file is as expected
    metadata_location = os.path.join(
        os.getcwd(), 'uploads', 'meta')
    metadata_file = os.path.join(metadata_location, f'{access_key_id}.json')
    assert os.path.isfile(metadata_file)
    with open(metadata_file, 'rb') as meta:
        metadata = json.loads(meta.read())
    assert metadata['filename'] == filename


def test_complete(testapp):
    # setup metadata from prior post
    metadata = dict(filename="snorlax.bin",
                    input_file_size=10, output_file_size=5)
    metadata_location = os.path.join(
        os.getcwd(), 'uploads', 'meta', 'snorlax.json')
    with open(metadata_location, 'w') as metadata_file:
        metadata_file.write(json.dumps(metadata))

    # GET show
    res = testapp.get('/complete?id=snorlax', status=200)
    assert b'Original Size' in res.body
    assert b'snorlax.bin' in res.body
