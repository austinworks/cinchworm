import os
from pyramid.view import view_config


@view_config(route_name='complete', renderer='cinchworm:templates/complete.jinja2')
def complete_upload(request):
    if 'safe_filename' in request.GET and os.path.isfile(os.path.join(os.getcwd(), 'uploads', request.GET['safe_filename'])):
        link = request.route_url('download', _query=dict(
            safe_filename=request.GET['safe_filename'],
            actual_filename='compressed_' + request.GET['filename']))
    else:
        link = None
    return {
        'original_size': float(request.GET.get('input_file_size', 1)),
        'final_size': float(request.GET.get('output_file_size', 1)),
        'filename': request.GET.get('filename', 'not submitted'),
        'link': link
    }
