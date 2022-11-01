import json
import os
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config


@view_config(route_name='complete', renderer='cinchworm:templates/complete.jinja2')
def complete_upload(request):
    metadata_path = os.path.join(os.getcwd(
    ), 'uploads', 'meta', '%s.json' % request.GET['id']) if 'id' in request.GET else None
    if metadata_path and os.path.isfile(metadata_path):
        with open(metadata_path) as metadata_file:
            metadata = json.loads(metadata_file.read())
        link = request.route_url('download', _query=dict(
            safe_filename='%s.bin' % request.GET['id'],
            actual_filename='compressed_' + metadata['filename']))
        return {
            'original_size': float(metadata['input_file_size']),
            'final_size': float(metadata['output_file_size']),
            'filename': metadata['filename'],
            'link': link
        }
    else:
        raise HTTPNotFound()
