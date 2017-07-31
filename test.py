from urlparse import urlparse
import simplejson
from rss2json import *
import json
import re


config=simplejson.loads(open("news.json").read())
#stringy = urlsource(config,"http://25livepub.collegenet.com/calendars/events_community.rss")
stringy = quotes(config)
print stringy
