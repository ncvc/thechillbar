from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import settings
import json
import simplejson
import datetime
import SignAnimator
import commands

# Hack to get lights working from here
import sys
# Path to bar_lighting and alphasign - specified in settings_local.py
sys.path.append(settings.DEPENDENCIES_PATH)
from bar_lighting import Strip, Animator

NUM_PIXELS = 32
UGC_LENGTH_LIMIT = 300

@csrf_exempt
@require_http_methods(['GET'])
def home(request):
    return filter('index.html', request, 'log.txt', '')
    
@csrf_exempt
@require_http_methods(['POST'])
def display(request):
    command = request.POST.get('command')[:UGC_LENGTH_LIMIT]
    if checkIP(request):
        Animator.sendMessage(command)
    return filter('index.html', request, 'displaylog.txt', command)

@csrf_exempt
@require_http_methods(['POST'])
def sign(request):
    message = request.POST.get('message')[:UGC_LENGTH_LIMIT]
    if request.method == "POST" and checkIP(request):
        SignAnimator.sendMessage(message.replace('\n', ''))
    return filter('index.html', request, 'signlog.txt', message)

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print "user not None"
            auth_login(request, user)
            return redirect("/")
        else:
            return render_to_response('login.html', {'login_error' : True}, context_instance=RequestContext(request))
    else:
        if request.user.is_authenticated():
            removeIPFromBanFile(getIP(request))
            return redirect("/")
        else:
            return render_to_response('login.html', {'login_error' : False}, context_instance=RequestContext(request))

def logout(request):
    auth_logout(request)
    return redirect('/')

@require_http_methods(['GET'])
def signlog(request):
    log_text = readSignLog()
    log_lines = log_text.split("POST")[1:]
    parsed_lines = []
    for line in log_lines:
        split_line = line.split()
        parsed_lines.append(split_line[:3] + [" ".join(split_line[3:])])

    bannedIPs = set(getBannedIPList())
    log = []
    for parsed_line in parsed_lines:
        log.append({'date' : parsed_line[0],
                    'time' : parsed_line[1],
                    'ip'   : parsed_line[2],
                    'message' : parsed_line[3],
                    'banned'  : parsed_line[2] in bannedIPs,
                    'self'    :  parsed_line[2] == getIP(request) })

    return HttpResponse(json.dumps(log), content_type="application/json")

@require_http_methods(['GET'])
def bannedips(request):
    results = [{'ip' : ip} for ip in getBannedIPList()]
    return HttpResponse(json.dumps(results), content_type="application/json")

@require_http_methods(['POST'])
@csrf_exempt
def ban(request):
    print "got request to ban ip {0}".format(request.POST.get('ip'))
    addIPToBanFile(request.POST.get('ip'))
    return HttpResponse(status=200)

@require_http_methods(['POST'])
@csrf_exempt
def unban(request):
    removeIPFromBanFile(request.POST.get('ip'))
    return HttpResponse(status=200)

def filter(filename, request, logfile, logtext):
    log = open(logfile, 'a+')
    log.write("{0} {1} {2} {3}\n".format(request.method, datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"), getIP(request), logtext))
    log.close()

    if checkIP(request):
        return render_to_response(filename, context_instance=RequestContext(request))
    else:
        return render_to_response('blacklist.html', context_instance=RequestContext(request))

def getBannedIPList():
    f = open('ip_blacklist.txt')
    lines = f.readlines()
    f.close()
    processed = set()
    result = [line.strip('\n') for line in lines if line not in processed and not processed.add(line)]
    return result

def addIPToBanFile(ip):
    f = open('ip_blacklist.txt', 'a+')
    f.write("{0}\n".format(ip))
    f.close()

def removeIPFromBanFile(ip):
    f = open('ip_blacklist.txt', 'r')
    banned_ips = f.read()
    f.close()
    f = open('ip_blacklist.txt', 'w')
    f.write(banned_ips.replace("{0}\n".format(ip), ""))
    f.close();

def readSignLog():
    status, output = commands.getstatusoutput("tac signlog.txt | grep 'POST' -m 15")
    if status == 0:
        return output
    else:
        return []

#returns True if OK, False if on blacklist
def checkIP(request):
    ip = getIP(request)
    if ip in set(getBannedIPList()):
        print "IP {0} is blacklisted".format(ip)
        return False
    return True

def getIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
