from django.urls import path

from . import views

urlpatterns = [
    path('EscapeRoute', views.get_escape_route_list, name='get_escape_route_list'),
    path('EscapeRoute/<int:escape_route_number>', views.get_escape_route, name='get_escape_route'),
    ]