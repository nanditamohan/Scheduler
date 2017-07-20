#!/usr/bin/env python
import feedparser
import re

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from bs4 import BeautifulSoup

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

def create_template(event_name, start_info, location, event_url, end_info="", description="", tags="", pic_url=""):
    """create .tmpl file to be used in main()
    required fields: event_name, start_info, location, event_url
    optional fields: end_info, description, tags, pic_url
    """

    #event_name = "entry."+event_name

    text = """"feed":
[
    {% for entry in feed %}
    {
        "weburl": "",
        "evtname": "{{entry."""+event_name+"""}}",
        "url": "{{ entry.""" + event_url + """}}",
        "location": "{{ entry.""" + location + """}}",
        "evtsource": "",
        "createdate": "",
        "evtdesc": "{{ entry.""" + description + """}}",
        "grps": ["{{ entry.""" + tags + """}}"],
        "endtime": "{{ entry.""" + end_info + """}}",
        "picurl": "{{ entry.""" + pic_url + """}}",
        "starttime": "{{ entry.""" + start_info + """}}"
    },
    {% endfor %}
]
"""
    with open('template.tmpl', 'w') as output:
        output.write(text)

def main():
    create_template("title", "category", "description", "link", "category" , "description", "title", "link")
    feed = feedparser.parse('http://25livepub.collegenet.com/calendars/events_community.rss')
    json = render_template(feed.entries, 'template.tmpl')
    json = parse_out_html_tags(json)
    json = decode_html_entities(json)
    with open('news.json', 'w') as output:
        output.write(json)

if __name__ == '__main__':
    main()
