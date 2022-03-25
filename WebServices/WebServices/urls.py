"""
Definition of urls for WebServices.
"""

from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from home import views as home_views
from home import forms as home_forms
from accounts import views as accounts_views
from dashboard import views as dashboard_views


urlpatterns = [
    path('GlobalAccess', home_views.home, name='home'),
    path('GlobalAccess/contact/', home_views.contact, name='contact'),
    path('GlobalAccess/about/', home_views.about, name='about'),
    path('GlobalAccess/dashboard/', include('dashboard.urls')),              # Including urls form dashboard app.
    path('GlobalAccess/api/', include('database_api.urls')),
    path('GlobalAccess/login/', accounts_views.login, name='login'),
    path('GlobalAccess/login_vs/',
         LoginView.as_view
         (
             template_name='home/login.html',
             authentication_form=home_forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login_vs'),
    path('GlobalAccess/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('GlobalAccess/admin/', admin.site.urls),
]
