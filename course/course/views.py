from django.shortcuts import render_to_response
from django.http import HttpResponse
import datetime
from courses.models import Student

def current_datetime(request):
    current_date = datetime.datetime.now()
    return render_to_response('current_datetime.html', locals())

def hello(request):
    return HttpResponse("Hello, World!")

def test_table(request):
    student_list = Student.objects.all()
    return render_to_response("test_table.html", locals())
