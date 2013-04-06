from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name = "Course Name")
    category = models.CharField(max_length=50, verbose_name = "Category")
    description = models.CharField(max_length=500, verbose_name="Course Description")
    startDate = models.DateField(verbose_name="Starting Date")
    endDate = models.DateField(verbose_name="Starting Date")
    students = models.ManyToManyField(User, through = "CourseEnrollment", related_name='%(app_label)s_%(class)s_related', verbose_name="Enrolled Students")
    instructors = models.ManyToManyField(User, through = "CourseInstructor",related_name='instructors', verbose_name="Instructor(s)")
    url = models.CharField(max_length=20, verbose_name="URL")
    def __unicode__(self):
        return self.name
        
class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name="Lesson Name")
    description = models.CharField(max_length=500, verbose_name="Lesson Description")
    number = models.IntegerField(verbose_name="Lesson Number")
    course = models.ForeignKey(Course, verbose_name="Course")
    
class CourseEnrollment(models.Model):
    student = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_related')
    course = models.ForeignKey(Course, related_name='%(app_label)s_%(class)s_related')
    date_enrolled = models.DateField()

class CourseInstructor(models.Model):
    instructor = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_related')
    course = models.ForeignKey(Course, related_name='the_course')
    date_joined = models.DateField()
