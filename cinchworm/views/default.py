from pyramid.view import view_config


@view_config(route_name='home', renderer='cinchworm:templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'Cinchworm', 'messages': request.session.pop_flash()}
