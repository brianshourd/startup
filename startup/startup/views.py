from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login, authenticate
#View function for main page. Renders index.html with no additional context.
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
    
#View function to handle registration. 
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
            return render_to_response("registration/register.html", {'errors': errors, 'name':request.POST['username'], 'sumName':request.POST['sumName'], 'email':request.POST['email']}, context_instance = RequestContext(request))
        #No errors, create user
        else:
            user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
            user.save()
            return render_to_response("registration/register.html", {'registered':True},context_instance = RequestContext(request)) 
    return render_to_response("registration/register.html", context_instance = RequestContext(request))

