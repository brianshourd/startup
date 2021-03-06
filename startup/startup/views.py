import re

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from course.models import Course, Lesson, CourseEnrollment, CourseInstructor

from datetime import date
#View function for main page. May render splash or index
def splash(request):
    #if request.user.is_authenticated():
        return render_to_response('index.html', context_instance=RequestContext(request))
    #else:
    #    return render_to_response('splash.html', context_instance=RequestContext(request))

#Always return the index page. Renders 'index.html' with no additional context. 
def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

#View function to handle user login. Renders 'login.html' with context 'error' if there was an error in log in
def auth_login(request):
    if request.method=="POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return render_to_response('registration/login.html', context_instance=RequestContext(request))
        else:
            return render_to_response('registration/login.html', {'error':'Invalid Username and Password'}, context_instance=RequestContext(request))
    else:
        return render_to_response('registration/login.html', context_instance=RequestContext(request))
    
#View function to display available courses. Renders 'courses/browse.html' with additional context
    #currentCourses = a list of currently available Course Objects
    #upcomingCourses = a list of upcoming Course objects
def browseCourses(request):
    return render_to_response('courses/browseDemo.html', context_instance=RequestContext(request))
    currentCourses = Course.objects.filter(startDate__lte = date.today())
    currentCourses =  currentCourses.exclude(endDate__lt = date.today())
    upcomingCourses = Course.objects.filter(startDate__gt = date.today())
    upcomingCourses= upcomingCourses.order_by('startDate')
    return render_to_response('courses/browse.html', {'currentCourses':currentCourses, 'upcomingCourses':upcomingCourses}, context_instance=RequestContext(request))
    
def demo(request):
    return render_to_response('courses/woodworkingCourse.html', context_instance=RequestContext(request))
    
def demoLesson(request):
    return render_to_response('courses/hand-tool-woodworkinLesson1.html', context_instance=RequestContext(request))
#View function to view a course page. Renders 'courses/viewCourseEnrolled.html' with context 'course' if the user is enrolled. 'courses/viewCourseSplash.html' with context course otherwise.
def viewCourse(request, courseURL):
    #try:
        print "YEP"
        course = Course.objects.get(url=courseURL)
        lessons = Lesson.objects.filter(course=course)
        if request.user in course.students.all():
            return render_to_response('courses/viewCourseEnrolled.html', {'course':course, 'lessons':lessons}, context_instance =RequestContext(request))
        else: #Render 'splash' page for the course
            return render_to_response('courses/viewCourseSplash.html', {'course':course, 'lessons':lessons},context_instance=RequestContext(request))        
   #except DoesNoExist:

def enroll(request, courseURL):
    course=Course.objects.get(url=courseURL)
    if request.user.is_authenticated():
        enrolled = CourseEnrollment.objects.filter(student=request.user, course=course)
        if enrolled:
            return render_to_response('courses/enroll.html', {'prevEnrolled':True, 'course':course}, context_instance=RequestContext(request))
        else:
            CourseEnrollment.objects.create(student=request.user, course = course, date_enrolled = date.today())
            return render_to_response('courses/enroll.html', {'justEnrolled':True, 'course':course}, context_instance=RequestContext(request))
    else:
        return render_to_response('courses/enroll.html', {'course':course}, context_instance=RequestContext(request))
        
#View to render a user's profile. 
def myCourses(request):
    if request.user.is_authenticated():
        courses = Course.objects.filter(students__username__exact = request.user.username)
        currentCourses =  courses.exclude(endDate__lt = date.today())
        pastCourses = courses.filter(endDate__lt = date.today())
        pastCourses= pastCourses.order_by('endDate')
        return render_to_response('myCourses.html', {'currentCourses':currentCourses, 'pastCourses':pastCourses}, context_instance = RequestContext(request))
    else:
        return render_to_response('myCourses.html', context_instance = RequestContext(request))
#View function to view a course page. 
def viewLesson(request, courseURL, lessonNumber):
    #try:
        course = Course.objects.get(url=courseURL)
        lesson = Lesson.objects.get(course=course, number = lessonNumber)
        if request.user.is_authenticated() and CourseEnrollment.objects.filter(course=course, student=request.user):
            return render_to_response('courses/%sLesson%d.html' %(course.url, lesson.number), {'course':course, 'lesson':lesson}, context_instance=RequestContext(request))
        else:
            return render_to_response('courses/%sLesson%d.html' %(course.url, lesson.number), {'course':course, 'lesson':lesson, 'notEnrolled': True}, context_instance=RequestContext(request)  )
   #except DoesNoExist:

#View function to handle registration. Renders 'registration/register.html' with additonal context:
    #errors - a list of validation errors for the form
    #name - the username previously entered if the validation failed
    #email - the email previously entered if the validation failed
    #registered - boolean value that is true if registration was successful
def register(request):
    if request.method == 'POST':
        #Validate inputs and create any errors
        errors=[]
        try:
            User.objects.get(username=request.POST['username'])
            errors+=['That username has already been taken']
        except User.DoesNotExist:
            pass
        if len(request.POST['username'])<4:
            errors+=['Your username must be between 4 and 16 characters']
        if len(request.POST['password'])<5:
            errors+=['Your password must be between 5 and 20 characters']
        if request.POST['password'] != request.POST['confirmPassword']:
            errors+=['Your passwords do not match']
        if request.POST['email'] =="":
            errors+=['Must enter an Email address']
        #Found an error
        if errors != []:
            return render_to_response("registration/register.html", {'errors': errors, 'name':request.POST['username'], 'email':request.POST['email']}, context_instance = RequestContext(request))
        #No errors, create user
        else:
            user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
            user.save()
            return render_to_response("registration/register.html", {'registered':True},context_instance = RequestContext(request)) 
    return render_to_response("registration/register.html", context_instance = RequestContext(request))

def teach(request):
    return render_to_response('courses/teach.html', context_instance=RequestContext(request))

#Search for courses, returns the courseSearch.html template with context
# The following code is for searching, taken from http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
def courseSearch(request):
#View function to handle the search in the navbar. Renders 'search_form'.html with context 'users'-a list of users matching the search query
# 'query'-a string of the query that was searched.
    if request.method=='GET':
        courses=Course.objects.filter(name__icontains=request.GET['query'])
    return render_to_response('courseSearch.html', {'courses':courses, 'query':request.GET['query']}, context_instance=RequestContext(request))  

#Pretends like the upload was a success, returning upload.html with context
def upload(request):
    return render_to_response('uploadSuccess.html', context_instance=RequestContext(request))

