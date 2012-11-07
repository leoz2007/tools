#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.template import loader
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import get_messages
from django.shortcuts import render_to_response, redirect
from django.template.loader_tags import BlockNode, ExtendsNode
from django.template import loader, Context, RequestContext, TextNode
from django.conf import settings
import ipdb
import logging, json, time, os
import simplejson as json
from datetime import datetime, date
from django.utils.dateformat import format

logger = logging.getLogger(__name__)
filename = "./site_media/travels.json"

def get_home(request):
    return render_to_response('home.html')

def get_revolution(request):
    return render_to_response('revolution.html')

def get_data(request):
    if request.is_ajax():
        travel = {}
        travel['from'] = request.GET['departure']
        travel['to'] = request.GET['arrival']
        travel['distance'] = request.GET['distance']
        file_content = ""
        try:
            fd = open(filename, "r")
            if os.stat(filename).st_size:
                file_content = fd.read()
                travels = json.loads(file_content)
            else:
                travels = []
            print travel
            travels.append(travel)
            print travels
            res = json.dumps(travels)
            fd.close()
            fd = open(filename,"w")
            fd.write(res)
            fd.close()
            return HttpResponse()
        except IOError as e:
            print "Error on views.py - no such file or directory"
            return HttpResponseForbidden()
    return HttpResponseForbidden()

def get_image(request):
    d = request.GET['d']
    a = request.GET['a']
    dist = request.GET['dist']
    total = request.GET['t']
    return render_to_response('image.html')
