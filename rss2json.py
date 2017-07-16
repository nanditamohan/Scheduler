#!/usr/bin/env python
import feedparser
import re

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

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

def create_template(link, name, start_date_and_time, location, event_url, end, description="", tags="", pic_url=""):
    """create .tmpl file to be used in main()"""
    

def main():
    feed = feedparser.parse('http://25livepub.collegenet.com/calendars/events_community.rss')        
    json = render_template(feed.entries, 'news.tmpl')
    json = parse_out_html_tags(json)
    with open('news.json', 'w') as output:
        output.write(json)

if __name__ == '__main__':
    main()