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

    args = [event_name, start_info, location, event_url, end_info, description, tags, pic_url]

    for elt in args:
        if elt != "":
            elt = "entry." + elt
    #event_name = "entry."+event_name

    text = """"feed":
[
    {% for entry in feed %}
    {
        "weburl": "",
        "evtname": "{{ """+ args[0] +"""}}",
        "url": "{{ """ + args[3] + """}}",
        "location": "{{ """ + args[2] + """}}",
        "evtsource": "",
        "createdate": "",
        "evtdesc": "{{""" + args[5] + """}}",
        "grps": ["{{ """ + args[6] + """}}"],
        "endtime": "{{ """ + args[4] + """}}",
        "picurl": "{{ """ + args[7] + """}}",
        "starttime": "{{ """ + args[1] + """}}"
    },
    {% endfor %}
]
"""
    with open('template.tmpl', 'w') as output:
        output.write(text)

def main():
    create_template("title", "category", "description", "link", "category" , "description", "title", "link")
    feed = feedparser.parse('http://nursing.jhu.edu/news-events/events/hopkins-nursing/rss')
    json = render_template(feed.entries, 'template.tmpl')
    json = parse_out_html_tags(json)
    json = decode_html_entities(json)
    with open('news.json', 'w') as output:
        output.write(json)

if __name__ == '__main__':
    main()
