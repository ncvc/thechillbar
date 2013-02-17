from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import settings
import simplejson
import datetime
import SignAnimator

# Hack to get lights working from here
import sys
# Path to bar_lighting and alphasign - specified in settings_local.py
sys.path.append(settings.DEPENDENCIES_PATH)
from bar_lighting import Strip, Animator

NUM_PIXELS = 32
UGC_LENGTH_LIMIT = 300

@csrf_exempt
def home(request):
    #GET requests return main page
    if request.method == "GET":
        return filter('index.html', request, '')
    
    #POST requests process posted data and perform LED actions
    if request.method == "POST":
        command = request.POST.get('command')[:UGC_LENGTH_LIMIT]
        if checkIP(request):
            Animator.sendMessage(command)
        return filter('index.html', request, command)
        
@csrf_exempt
def sign(request):
    message = request.POST.get('message')[:UGC_LENGTH_LIMIT]
    if request.method == "POST" and checkIP(request):
        SignAnimator.sendMessage(message.replace('\n', ''))
    return filter('index.html', request, message)

#returns True if OK, False if on blacklist
def checkIP(request):
    ip = getIP(request)
    f = open('ip_blacklist.txt')
    if ip in f.read():
    	f.close()
        print 'IP %s blocked by blacklist' % ip
        return False
    f.close()
    return True

def getIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def filter(filename, request, logtext):
    log = open('log.txt', 'a+')
    log.write("{0} {1} {2} {3}\n".format(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"), request.method, getIP(request), logtext))
    log.close()

    if checkIP(request):
        return render_to_response(filename, context_instance=RequestContext(request))
    else:
        return render_to_response('blacklist.html', context_instance=RequestContext(request))
