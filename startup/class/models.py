from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    startDate = models.DateField()
    endDate = models.DateField()
    students = models.ManyToManyField(User, through = "CourseEnrollment", related_name='%(app_label)s_%(class)s_related')
    instructors = models.ManyToManyField(User, through = "CourseInstructor",related_name='instructors')
    def __unicode__(self):
        return self.name
        
class Lesson(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    
class CourseEnrollment(models.Model):
    student = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_related')
    course = models.ForeignKey(Course, related_name='%(app_label)s_%(class)s_related')
    date_enrolled = models.DateField()

class CourseInstructor(models.Model):
    instructor = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_related')
    course = models.ForeignKey(Course, related_name='the_course')
    date_joined = models.DateField()
