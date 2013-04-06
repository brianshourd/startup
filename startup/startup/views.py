from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from course.models import Course, Lesson, CourseEnrollment, CourseInstructor

from datetime import date
#View function for main page. May render splash or index
def splash(request):
    if request.user.is_authenticated():
        return render_to_response('index.html', context_instance=RequestContext(request))
    else:
        return render_to_response('splash.html', context_instance=RequestContext(request))

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
    currentCourses = Course.objects.filter(startDate__lte = date.today())
    currentCourses =  currentCourses.exclude(endDate__lt = date.today())
    upcomingCourses = Course.objects.filter(startDate__gt = date.today())
    upcomingCourses= upcomingCourses.order_by('startDate')
    return render_to_response('courses/browse.html', {'currentCourses':currentCourses, 'upcomingCourses':upcomingCourses}, context_instance=RequestContext(request))
    
#View function to view a course page. 
def viewCourse(request, courseURL):
    #try:
        course = Course.objects.get(url=courseURL)
        if request.user in course.students.all():
            return render_to_response('courses/viewCourseEnrolled.html', context_instance =RequestContext(request))
        else: #Render 'splash' page for the course
            return render_to_response('courses/viewCourseSplash.html', {'course':course},context_instance=RequestContext(request))        
   #except DoesNoExist:

#View function to view a course page. 
def viewLesson(request, courseURL, lessonNumber):
    #try:
        course = Course.objects.get(url=courseURL)
        if request.user in course.students.all():
            return render_to_response('courses/viewCourseEnrolled.html', context_instance =RequestContext(request))
        else: #Render 'splash' page for the course
            return render_to_response('courses/viewCourseSplash.html', {'course':course},context_instance=RequestContext(request))        
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

