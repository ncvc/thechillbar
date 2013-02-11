from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import settings
import simplejson
import SignAnimator

# Hack to get lights working from here
import sys
sys.path.append('/home/pi/')
from bar_lighting import Strip, Animator

NUM_PIXELS = 32
UGC_LENGTH_LIMIT = 300

@csrf_exempt
def home(request):
    blacklisted = checkIP(request)

    #GET requests return main page
    if request.method == "GET" and not blacklisted:
        return filter('index.html', request, blacklisted)
    
    #POST requests process posted data and perform LED actions
    if request.method == "POST":
        command = request.POST.get('command')[:UGC_LENGTH_LIMIT]
        print getIP(request), command
        if not blacklisted:                         
            Animator.sendMessage(command)
        return filter('index.html', request, blacklisted)
        
@csrf_exempt
def sign(request):
    blacklisted = checkIP(request)
    
    message = request.POST.get('message')[:UGC_LENGTH_LIMIT]
    print getIP(request), message

    if request.method == "POST" and not blacklisted:
        SignAnimator.sendMessage(message)

    return filter('index.html', request, blacklisted)

def checkIP(request):
    ip = getIP(request)

    last_ips = open('past_ips.txt', 'a+')
    last_ips.write(ip + '\n')
    last_ips.close()

    f = open('ip_blacklist.txt')
    
    if ip in f.read():
    	f.close()
        print 'IP %s blocked by blacklist' % ip
        return True
    f.close()
    return False

def getIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip    

def filter(filename, request, blacklisted):
    if blacklisted:
        return render_to_response('blacklist.html', context_instance=RequestContext(request))
    else:
        return render_to_response(filename, context_instance=RequestContext(request))
