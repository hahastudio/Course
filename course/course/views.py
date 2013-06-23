from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
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

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/test_table/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/loggedout/")