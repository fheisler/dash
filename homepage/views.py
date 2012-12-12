from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django import forms
from django.core.exceptions import ValidationError

from homepage.models import UserProfile
from homepage.forms import SettingsForm, ZipField

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#from django.utils.encoding import smart_text

from homepage.news import NewsArticle, Event, Item
from datetime import datetime, timedelta
import urllib, urllib2
import json, re

'''
# Cannot import WordNet corpora non-locally
try: # use WordNet if available
    from nltk.corpus import wordnet as wn
except ImportError:
    pass
'''

MAX_ITEMS= 24

def hackEncode(text):
    hacks = {
        "&ldquo;": '"'
        ,"&rdquo;": '"'
        ,"&#x22;": '"'
        ,"&#x201C;": '"'
        ,"&rsquo;": "'"
        ,"&#x2018;": "'"
        ,"&#x2019;": "'"
        ,"&#x27;": "'"
        ,"&mdash;": "-"
        ,"&#x2014;": "-"
        ,"&#xa;": " "
        ,"&#x201D;": ","
        }
    rc = re.compile('|'.join(map(re.escape, hacks)))
    def translate(match):
        return hacks[match.group(0)]
    return rc.sub(translate, text)

def rank(items, interests):
    # get most common synonyms
    terms = []
    for interest in interests:
        terms.append(interest)
        '''
        try: # has nltk
            synsets = wn.synsets(interest)
            if len(synsets) > 0:
                terms += synsets[0].lemma_names
        except NameError:
            pass
        '''

    # assign ranks, then re-order descending by rank
    for item in items:
        # give a point for every synonym hit
        score = 0
        for term in terms:
            score += item.title.count(term)
            score += item.body.count(term)
        item.setRank(score)
    items.sort(key=lambda x: x.rank, reverse=True)
    if len(items) > MAX_ITEMS:
        items = items[:MAX_ITEMS]
    return items

def index(request):
    ''' main dashboard view '''
    if request.user.is_authenticated():
        interests = request.user.get_profile().list_interests()
        zipcode = request.user.get_profile().zipcode
    else:
        interests = []
    
    now = datetime.now()
    prev_mo = now - timedelta(days=30)
    next_mo = now + timedelta(days=30)
    
    items = []
    for interest in interests:
        # read the NYT
        news_url = "http://api.nytimes.com/svc/search/v1/article?begin_date={begin_date}&end_date={end_date}&fields=body,title,url,date&api-key=c86fea7514da37e1f547c73d654fa268:11:61438929&query={query}".format(
            begin_date = prev_mo.strftime("%Y%m%d")
            ,end_date = now.strftime("%Y%m%d")
            ,query = urllib.quote_plus(interest))
        try:
            news_result = urllib2.urlopen(news_url)
        except urllib2.HTTPError:
            pass
        else:
            newsDict = json.loads(news_result.read())
            for article in newsDict["results"]:
                #title = smart_text(article["title"]) #TODO: dumb_text
                title = article["title"]
                title = hackEncode(title)
                url = article["url"]
                source = "New York Times"
                #body = smart_text(article["body"]) #TODO: dumb_text
                body = article["body"]
                p = re.compile(r'<.*?>')
                body = p.sub('', body)
                body = hackEncode(body)
                if len(body) > 200:
                    body = body[:200] + "..."
                date = article["date"]
                items.append(NewsArticle(title, url, source, body, date))

        # scrape EventBrite
        eventquery = " AND ".join(interest)
        events_url = "https://www.eventbrite.com/json/event_search?app_key=NXYH4QJ4WB3HIJNB5P&date={begin_date}%20{end_date}&postal_code={postal_code}&within=25&keywords={query}".format(
            begin_date=now.strftime("%Y-%m-%d")
            ,end_date=next_mo.strftime("%Y-%m-%d")
            ,postal_code = zipcode
            ,query = urllib.quote_plus(eventquery))
        try:
            events_result = urllib2.urlopen(events_url)
        except urllib2.HTTPError:
            pass
        else:
            eventsDict = json.loads(events_result.read())
            for event in eventsDict["events"]:
                if "event" in event:
                    title = event["event"]["title"]
                    title = hackEncode(title)
                    url = event["event"]["url"]
                    source = "Eventbrite"
                    body = event["event"]["description"]
                    p = re.compile(r'<.*?>')
                    body = p.sub('', body)
                    body = hackEncode(body)
                    if len(body) > 200:
                        body = body[:200] + "..."
                    date = event["event"]["start_date"]
                    items.append(Event(title, url, source, body, date))
    
    # re-order and limit items
    items = rank(items, interests)
    
    context = {}
    context["items"] = items
    return render(request, 'index.html', context)


@login_required
def settings(request):
    ''' user settings page '''
    context = {}
    context["interests"] = request.user.get_profile().interests
    
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            # process submitted form
            #interests = [i for i in request.POST['interests'].split(",")]
            interests = request.POST['interests']
            if interests != '':
                request.user.get_profile().interests = interests
            else:
                request.user.get_profile().interests = None
            request.user.first_name = request.POST['firstname']
            request.user.last_name = request.POST['lastname']
            request.user.email = request.POST['email']
            request.user.get_profile().zipcode = int(request.POST['zipcode'])
            request.user.save()
            request.user.get_profile().save()
            return HttpResponseRedirect('/')
    else:
        # set up unbound form
        initial = {
            'interests': request.user.get_profile().interests
            ,'firstname': request.user.first_name
            ,'lastname': request.user.last_name
            ,'email': request.user.email
            ,'zipcode': request.user.get_profile().zipcode
            }
        if initial['zipcode'] == None:
            initial['zipcode'] = "20500"
            #TODO: read in best guess via location services
        form = SettingsForm(initial=initial)

    context['form'] = form
    context['interest_list'] = request.user.get_profile().list_interests()
    return render(request, 'settings.html', context)

def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/user/login')
