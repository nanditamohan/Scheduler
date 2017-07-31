#!/usr/bin/env python
import feedparser
import re
from urlparse import urlparse

from jinja2 import Environment
#from jinja2 import Template
from jinja2.loaders import FileSystemLoader
from bs4 import BeautifulSoup
import json

def render_template(data, template_name, filters=None):
    """Render data using a jinja2 template"""
    env = Environment(loader=FileSystemLoader(''))

    if filters is not None:
        for key, value in filters.iteritems():
            env.filters[key] = value

    template = env.get_template(template_name)
    return template.render(feed=data).encode('utf-8')

def parse_out_html_tags(string):
    toclean = re.compile('<.*?>')
    cleantext = re.sub(toclean, '',string)
    return cleantext

def decode_html_entities(string):
    decodedtext = BeautifulSoup(string)
    return decodedtext.text.encode('utf-8')

def urlsource(jsonlink):
    """Goes through json and makes "evtsource" contain the parsed hostname"""
    #jsonlist = json.loads(jsonlink) #to remove blank lines
    for dict in jsonlink:
        try:
            dict["evtsource"]=urlparse(dict["evtsource"]).hostname
        except KeyError:
            pass
    return jsonlink

def quotes(jsonfull):
    """Converts quotes inside json VALUE to be opposite of what it starts & ends with"""
    #that's what is causing all our errors


def create_template(rsslink, event_name, start_info, location, event_url, end_info="", description="", tags="", pic_url=""):
    """create .tmpl file to be used in main()
    required fields: event_name, start_info, location, event_url
    optional fields: end_info, description, tags, pic_url
    """

    args = [event_name, start_info, location, event_url, end_info, description, tags, pic_url]
    #evtsource = urlfind.hostname #need to paste this next to evtsource
    #print evtsource
    for i in range(len(args)):
        if (args[i] != ""):
            args[i] = "entry." + args[i]
    #event_name = "entry."+event_name
    """CHECKS that event_url is not empty so it can parse out
    evtsource from the link - check fct. parselink() below, which can be called
    in the template for urlfind"""
    if(args[3] != ""):
        urlfind = args[3]
    else:
        urlfind=""

    text = """[
    {% for entry in feed %}
    {
        "weburl": "",
        "evtname": "{{ """+ args[0] +"""}}",
        "url": "{{ """ + args[3] + """}}",
        "location": "{{ """ + args[2] + """}}",
        "evtsource": "{{"""+urlfind+"""}}",
        "createdate": "",
        "evtdesc": "{{""" + args[5] + """}}",
        "grps": ["{{ """ + args[6] + """}}"],
        "endtime": "{{ """ + args[4] + """}}",
        "picurl": "{{ """ + args[7] + """}}",
        "starttime": "{{ """ + args[1] + """}}"
    },
    {% endfor %}
]"
"""
    with open('template.tmpl', 'w') as output:
        output.write(text)


def main():
    create_template("title", "title", "description", "link", "category" , "description", "title","link")
    feed = feedparser.parse('http://25livepub.collegenet.com/calendars/events_community.rss')
    json = render_template(feed.entries, 'template.tmpl')
    json = parse_out_html_tags(json)
    json = decode_html_entities(json)
    json = urlsource(json)
    with open('news.json', 'w') as output:
        output.write(json)

if __name__ == '__main__':
    main()
