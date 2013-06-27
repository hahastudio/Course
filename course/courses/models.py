#coding:utf-8
from django.db import models

# Create your models here.
class Time(models.Model):
    """docstring for Time"""
    WEEKS = (
        ("Sun", u"星期日"),
        ("Mon", u"星期一"),
        ("Tue", u"星期二"),
        ("Wed", u"星期三"),
        ("Thu", u"星期四"),
        ("Fri", u"星期五"),
        ("Sat", u"星期六"),
        )
    REPEAT_TYPES = (
        (u"单周", u"单周"),
        (u"双周", u"双周"),
        (u"每周", u"每周"),
        )
    
    start_week = models.PositiveIntegerField()
    end_week = models.PositiveIntegerField() #remember to check end_week > start_week
    week = models.CharField(max_length=3, choices=WEEKS)
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField() #remember to check end_time > start_time
    repeat_type = models.CharField(max_length=4, choices=REPEAT_TYPES)
    address = models.CharField(max_length=20)

    def __unicode__(self):
    	return u"(%d-%d周) %s %s %d-%d节 %s" % (self.start_week, self.end_week, self.get_repeat_type_display(), self.get_week_display(), self.start_time, self.end_time, self.address)

    def save(self, *args, **kwargs):
        if self.end_week > self.start_week:
            if self.end_time > self.start_time:
                super(Time, self).save(*args, **kwargs)
            else:
                raise Exception("end_time should be greater than start_time")
        else:
            raise Exception("end_week should be greater than start_week")

class Teacher(models.Model):
    """docstring for Teacher"""
    GENDERS = (
        ("M", u"男性"),
        ("F", u"女性"),
        )

    work_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDERS)
    age = models.PositiveIntegerField()
    academic_degree = models.CharField(max_length=10)
    positional_title = models.CharField(max_length=10)
    school = models.CharField(max_length=20)

    def __unicode__(self):
        return u"%s %s" % (self.work_id, self.name)

    class META:
        ordering = ['work_id']

class Student(models.Model):
    """docstring for Student"""
    GENDERS = (
        ("M", u"男性"),
        ("F", u"女性"),
        )
    YEAR_IN_SCHOOL_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
        )

    student_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDERS)
    age = models.PositiveIntegerField()
    school = models.CharField(max_length=20)
    major = models.CharField(max_length=20)
    grade = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
    class_in = models.CharField(max_length=10)

    def __unicode__(self):
        return u"%s %s %s" % (self.class_in, self.student_id, self.name)

    class META:
        ordering = ['student_id']

class Course(models.Model):
    """docstring for Course"""
    course_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    times = models.ManyToManyField(Time)
    credit = models.PositiveIntegerField()
    least_students = models.PositiveIntegerField()
    teacher = models.ForeignKey(Teacher)
    students = models.ManyToManyField(Student)

    def __unicode__(self):
        return u"%s, %s" % (self.course_id, self.name)

    class META:
        ordering = ['course_id']





        