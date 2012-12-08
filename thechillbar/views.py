from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import settings

# Hack to get lights working from here
import sys
sys.path.append('/home/pi/')
from bar_lighting import Strip

NUM_PIXELS = 32

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

        strip = Strip.Strip(NUM_PIXELS)
    
        #animation handling
        if request.POST.has_key("animation"):
            animator = Strip.Animations(strip)
            animation = request.POST.has_key("animation")

            if animation == "rainbow_cycle":
                animator.rainbowCycle()
            elif animation == "rainbow":
                animatorx.rainbowCycle()

        #set r, g, b values directly
        if request.POST.has_key('r') and request.POST.has_key('g') and request.POST.has_key('b'):
            try:
                #constrain to 0 <= r, g, b <= 127
                r = min(max(0, int(request.POST['r'])), 127)
                g = min(max(0, int(request.POST['g'])), 127)
                b = min(max(0, int(request.POST['b'])), 127)
                strip.setColor([r, g, b])
                strip.show()

            except Exception:
                print Exception

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
    if ip in f:
    	print 'IP %s blocked by blacklist' % ip
    	return render_to_response('blacklist.html', context_instance=RequestContext(request))
    print ip
    return None
