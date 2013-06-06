from django.shortcuts import render_to_response
from django.http import HttpResponse
import datetime

def current_datetime(request):
    current_date = datetime.datetime.now()
    return render_to_response('current_datetime.html', locals())

def hello(request):
    return HttpResponse("Hello, World!")
