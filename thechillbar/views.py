from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import settings

def home(request):
    print settings.STATIC_ROOT
    return render_to_response('index2.html', context_instance = RequestContext(request))
