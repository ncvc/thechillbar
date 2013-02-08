from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import settings
import simplejson

# Hack to get lights working from here
import sys
sys.path.append('/home/pi/')
from bar_lighting import Strip, Animator

NUM_PIXELS = 32

@csrf_exempt
def home(request):
    #blacklist filtering
    resp = checkIP(request)
    if resp != None:
    	return resp

    #GET requests return main page
    if request.method == "GET":
        return render_to_response('index2.html', context_instance=RequestContext(request))
    
    #POST requests process posted data and perform LED actions
    if request.method == "POST":
        Animator.sendMessage(request.POST.get('command'))
        return render_to_response('index2.html', context_instance=RequestContext(request))

def checkIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    last_ips = open('past_ips.txt', 'a+')
    last_ips.write(ip + '\n')

    f = open('ip_blacklist.txt')
    
    if ip in f.read():
    	print 'IP %s blocked by blacklist' % ip
    	return render_to_response('blacklist.html', context_instance=RequestContext(request))
    print ip
    return None
