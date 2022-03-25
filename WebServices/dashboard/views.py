from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.
def dashboard(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'dashboard.html')
