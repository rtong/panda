import pdb
import re
import random
import logging
import simplejson
from datetime import datetime
from operator import itemgetter
from django.http import HttpResponse
from django.template import RequestContext
from django.core.cache import get_cache, cache
from django.shortcuts import render_to_response
from lib.mem import *

EXPIRY_TIME = 100000
rv = get_cache('events')

logg = logging.getLogger("travelLogger")
logg_stats = logging.getLogger("travelLoggerSTATS")

def home_temp(request):
    data = {'key': 'value'}
    return render_to_response('home/events.html',{'data': data }, RequestContext(request, { }) )

def home(request):
    """
    When user hits home page, 
    """
    logg_stats.info("Events\t%s\tHome" % ( request.user.username))
    #Default value to be shown in the home page
    hashes_list = rv._client.zrange(name="total", start=0, end=400, desc=False)
    #Convert default to presentable type
    data = answer(hashes_list, '')
    return render_to_response('home/events.html',{'data': [data,'sela']}, RequestContext(request, { }) )

def home_map(request):
    """
    When the home page has a map
    """
    logg_stats.info("Events\t%s\tHome" % ( request.user.username))
    hashes_list = rv._client.zrange(name="total", start=0, end=400, desc=False)
    data = answer(hashes_list, '')
    return render_to_response('home/events_map.html',{'data': [data,'sela']}, RequestContext(request, { }) )

def event_search(request):
    """
    Search algorithm
    """
    try:
        if (request.GET.has_key('search')):
            searchWord = request.GET['search'].lower()
            logg_stats.info("Events\t%s\tKeyword\t%s" % ( request.user.username, searchWord))

            # Call search engine
            airList  = answer_fb(searchWord)
            result = [ airList, searchWord ]

            json = simplejson.dumps(result)
            return HttpResponse(json)
        else:
            return HttpResponse('{"result":"failed","desc":"No Matches Found"}')
    except Exception,e:
        logg_stats.critical(str(e))
        return HttpResponse('{"result":"failed","desc":"No Matches Found"}')

def event_desc(request):
    """
    User hits this method when he ask for description 
    regarding an event.
    """
    try:
        if (request.GET.has_key('eventid')):
            # Event id
            eventid = request.GET['eventid'].lower()
            logg_stats.info("EventsDesc\t%s\tKeyword\t%s" % ( request.user.username, eventid))

            airList  = answer_desc([eventid])
            result = [ airList, eventid ]

            json = simplejson.dumps(result)
            return HttpResponse(json)
        else:
            return HttpResponse('{"result":"failed","desc":"No Matches Found"}')
    except Exception,e:
        logg_stats.critical(str(e))
        return HttpResponse('{"result":"failed","desc":"No Matches Found"}')

def answer_fb(words):
    """
    All the sentences corresponding
    to the hashes dreived
    """
    uid = str(random.randint(1,100))
    set_list = ["t:%s"%word for word in words.split(' ')]
    res = rv._client.zinterstore("res"+uid, set_list)
    hashes_list = rv._client.zrange(name="res"+uid, start=0, end=400, desc=False)
    return answer(hashes_list, words)

def answer(hashes_list, words):
    """
    Used in case of gist of the event. 
    No descriptio is provided
    """
    suggList = []
    for hashes in hashes_list:
        di = {}
        result = rv._client.hget("t", hashes)
        data = rv._client.hgetall(hashes)
        """
        for word in words.split(' '):
            result = re.sub(r'(?i)%s'%word, '<span>'+word+'</span>', result)
        """
        # Name of the event
        di['name'] = data['n']
        di['event_id'] = hashes
        dtime = data['c']
        ctime = datetime.strptime(dtime, '%Y-%m-%d %H:%M:%S')
        di['month'] = ctime.strftime("%B")
        # Day of the date
        di['day'] = ctime.day
        # Start time of event
        di['stime'] = (dtime.split(' ')[1][:5]).replace(":","")
        # Location
        di['loc'] = data['lc'][:5]
        # Latitude
        di['lat'] = data['lt']
        # Longitude
        di['lon'] = data['ln']
        # City
        di['city'] = data['cy']
        di['meta'] = eval(data['mt'])
        suggList.append(di)
    return suggList

def answer_desc(hashes_list):
    """
    Creates the description in the json format
    """
    di = {}
    for hashes in hashes_list:
        result = rv._client.hget("t", hashes)
        data = rv._client.hgetall(hashes)
        """
        for word in words.split(' '):
            result = re.sub(r'(?i)%s'%word, '<span>'+word+'</span>', result)
        """
        # Starting 20 characters of the name is taken.
        di['name'] = data['n'][:20]
        di['event_id'] = hashes
        dtime = data['c']
        ctime = datetime.strptime(dtime, '%Y-%m-%d %H:%M:%S')
        di['month'] = ctime.strftime("%B")[:3]
        di['day'] = ctime.day
        di['stime'] = (dtime.split(' ')[1][:5]).replace(":","")
        # Location
        di['loc'] = data['lc'][:5]
        # Latitude
        di['lat'] = data['lt']
        # Longitude
        di['lon'] = data['ln']
        # Description about event
        di['desc'] = data['d']
        logg_stats.info("EventsDesc\t%s\tKeyword\t%s" % ( hashes, data['n']))
    return di
