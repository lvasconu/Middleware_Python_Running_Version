from django.shortcuts import render

def get_escape_route_list(request):

    context = {'escape_route_list': 'Pediu lista de rotas'}

    return render(request, 'database_api/index.html', context)


def get_escape_route(request, escape_route_number):
    assert isinstance(request, HttpRequest)

    query_dict = f'Pediu rota: {escape_route_number}'

    return render(request, '', query_dict)
