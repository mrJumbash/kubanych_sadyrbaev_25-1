from django.shortcuts import redirect, HttpResponse
from datetime import datetime

# Create your views here.

def bye_view(request):
    if request.method == 'GET':
        return HttpResponse('Goodby user!')

def hello_view(request):
    if request.method == 'GET':
        return HttpResponse('Hello! Its my project')

def date_view(request):
    if request.method == 'GET':
        return HttpResponse(f'{datetime.now()}')