#coding:utf-8
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import datetime
from courses.models import Student, Teacher, Course, Time
from django import forms

def current_datetime(request):
    current_date = datetime.datetime.now()
    return render_to_response('current_datetime.html', locals())

def hello(request):
    return HttpResponse("Hello, World!")

@login_required
def teacher_profile(request):
    teacher = Teacher.objects.get(work_id=request.user.username)
    courses = Course.objects.filter(teacher=teacher)
    return render_to_response('teacher/profile.html', {"name":teacher.name, "courses":courses})

class create_course_form(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('teacher', 'students', )

    def clean_course_id(self):
        course_id = self.cleaned_data['course_id']
        search_result = Course.objects.filter(course_id=course_id)
        if search_result:
            raise forms.ValidationError(u"该课号已被使用！")
        return course_id

class edit_course_form(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('course_id', 'teacher', 'students', 'times')

@login_required
@csrf_protect
def create_course(request):
    if request.user.groups.all()[0].name == "Teacher":
        if request.method == 'POST':
            teacher = Teacher.objects.get(work_id=request.user.username)
            course_form = create_course_form(request.POST)
            if course_form.is_valid():
                cd = course_form.cleaned_data
                course_id = cd['course_id']
                name = cd['name']
                credit = cd['credit']
                least_students = cd['least_students']
                new_course = Course(course_id=course_id, name=name, credit=credit, least_students=least_students, teacher=teacher)
                new_course.save()
                for time in cd['times']:
                    new_course.times.add(time)
                return HttpResponseRedirect('/teacher/profile/')
        else:
            course_form = create_course_form()
        return render(request, 'teacher/create_course.html', {'course_form': course_form})
    else:
        return render(request, "accounts/login.html")

@login_required
@csrf_protect
def view_course(request, course_id):
    if request.user.groups.all()[0].name == "Teacher":
        try:
            course = Course.objects.get(course_id=course_id)
        except Course.DoesNotExist:
            return HttpResponseRedirect('/teacher/profile/')
        teacher = Teacher.objects.get(work_id=request.user.username)
        if course.teacher == teacher:
            return render(request, 'teacher/view_course.html', {'course_id':course.course_id, 'course_name':course.name, 'students':course.students.all()})
        else:
            return HttpResponseRedirect('/teacher/profile/')
    else:
        return render(request, "accounts/login.html")

@login_required
@csrf_protect
def edit_course(request, course_id):
    if request.user.groups.all()[0].name == "Teacher":
        try:
            course = Course.objects.get(course_id=course_id)
        except Course.DoesNotExist:
            return HttpResponseRedirect('/teacher/profile/')
        teacher = Teacher.objects.get(work_id=request.user.username)
        if course.teacher == teacher:
            if request.method == 'POST':
                course_form = edit_course_form(request.POST)
                if course_form.is_valid():
                    cd = course_form.cleaned_data
                    name = cd['name']
                    credit = cd['credit']
                    least_students = cd['least_students']
                    Course.objects.filter(course_id=course_id).update(name=name, credit=credit, least_students=least_students)
                    return HttpResponseRedirect('/teacher/profile/')
            else:
                course_form = edit_course_form(initial={'name':course.name, 'credit':course.credit, 'least_students':course.least_students})
            return render(request, 'teacher/edit_course.html', {'course_form': course_form})
    else:
        return render(request, "accounts/login.html")

@login_required
def student_profile(request):
    student = Student.objects.get(student_id=request.user.username)
    courses = Course.objects.filter(students__in = [student])
    return render(request, 'student/profile.html', {"name":student.name, "courses":courses})

@login_required
def choose_course_view(request):
    if request.user.groups.all()[0].name == 'Student':
        student = Student.objects.get(student_id=request.user.username)
        courses = Course.objects.all()
        courses_chosen = Course.objects.filter(students__in = [student])
        return render(request, 'student/choose_course.html', {"courses":courses, "courses_chosen":courses_chosen})
    else:
        return render(request, "accounts/login.html")

@login_required
def choose_course_act(request, course_id):
    if request.user.groups.all()[0].name == 'Student':
        try:
            chosen_course = Course.objects.get(course_id=course_id)
        except Course.DoesNotExist:
            return HttpResponseRedirect('/student/choose_course/')
        student = Student.objects.get(student_id=request.user.username)
        courses_chosen = Course.objects.filter(students__in = [student])
        if chosen_course in courses_chosen:
            return HttpResponseRedirect('/student/choose_course/')
        chosen_course.students.add(student)
        return HttpResponseRedirect('/student/profile/')
    else:
        return render(request, "accounts/login.html")

@login_required
def kick_course_view(request):
    if request.user.groups.all()[0].name == 'Student':
        student = Student.objects.get(student_id=request.user.username)
        courses = Course.objects.filter(students__in = [student])
        return render(request, 'student/kick_course.html', {"courses":courses})
    else:
        return render(request, "accounts/login.html")

@login_required
def kick_course_act(request, course_id):
    if request.user.groups.all()[0].name == 'Student':
        try:
            chosen_course = Course.objects.get(course_id=course_id)
        except Course.DoesNotExist:
            return HttpResponseRedirect('/student/kick_course/')
        student = Student.objects.get(student_id=request.user.username)
        courses = Course.objects.filter(students__in = [student])
        if chosen_course in courses:
            chosen_course.students.remove(student)
            return HttpResponseRedirect('/student/profile/')
        else:
            HttpResponseRedirect('/student/kick_course/')
    else:
        return render(request, "accounts/login.html")


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            if user.groups.all()[0].name == "Teacher":
                return HttpResponseRedirect("/teacher/profile/")
            elif user.groups.all()[0].name == "Student":
                return HttpResponseRedirect("/student/profile/")
        else:
            # Show an error page
            return HttpResponseRedirect("/accounts/login/")
    else:
        return render(request, "accounts/login.html")
    

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/loggedout/")