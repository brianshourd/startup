from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

#View function for main page. Renders index.html with no additional context.
def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))