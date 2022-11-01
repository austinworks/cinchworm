import os
from pyramid.view import view_config
from pyramid.response import FileResponse


@view_config(route_name='download')
def download_compressed_file(request):
    file_path = os.path.join(os.getcwd(), 'uploads',
                             request.GET['safe_filename'])

    dl_filename = request.GET['actual_filename']
    response = FileResponse(
        file_path,
        request=request,
        content_type='application/octet-stream'
    )
    response.headers['Content-Disposition'] = (
        f'attachment;  filename={dl_filename}')
    return response
