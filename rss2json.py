#!/usr/bin/env python
import feedparser
import re
from urlparse import urlparse

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from bs4 import BeautifulSoup
import json
import simplejson

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

def urlsource(jsonlink,rsslink):
    """Goes through json and makes "evtsource" contain the parsed hostname"""
    jsonlist = simplejson.loads(jsonlink, strict = False) #to remove blank lines
    for dict in jsonlist:
        try:
            dict["weburl"]=rsslink
            dict["evtsource"]=urlparse(dict["evtsource"]).hostname
        except KeyError:
            pass
    jsonlist = json.dumps(jsonlist, indent = 2)
    return jsonlist

def quotes(jsonfull):
    """Converts double quotes within JSON object to single quotes"""
    # replace double quotes between the third double quote and the last double quote with single quotes
    
    """
    def find_2nd(string, substring):
   return string.find(substring, string.find(substring) + 1)
    """
    returnstring = ''
    fullline = ''
    for line in jsonfull.splitlines():
        if line.count('"') > 4: 
            withoutfirstquote = line[line.find('"') + 1:]
            fullline = line[0:line.find('"')+1]
            withoutsecondquote = withoutfirstquote[withoutfirstquote.find('"') + 1:]
            fullline = fullline + withoutfirstquote[0:withoutfirstquote.find('"')+1]
            withoutthirdquote = withoutsecondquote[withoutsecondquote.find('"') + 1:]
            fullline = fullline + withoutsecondquote[0:withoutsecondquote.find('"')+1]
            dequoteArea = withoutthirdquote[0:withoutthirdquote.rfind('"')]
            dequoteArea = dequoteArea.replace('"', "'")
            fullline = fullline + dequoteArea + withoutthirdquote[withoutthirdquote.rfind('"'):]
        else:
            fullline = line
        returnstring += fullline + "\n"
        fullline = ''
    return returnstring

def create_template(event_name, start_info, location, event_url, end_info="", description="", tags="", pic_url=""):
    """create .tmpl file to be used in main()
    required fields: event_name, start_info, location, event_url
    optional fields: end_info, description, tags, pic_url
    """

    args = [event_name, start_info, location, event_url, end_info, description, tags, pic_url]

    for i in range(len(args)):
        if (args[i] != ""):
            args[i] = "entry." + args[i]
    #event_name = "entry."+event_name

    if(args[3] != ""):
        urlfind = args[3]
    else:
        urlfind=""


    text = """
[
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
]
"""
    with open('template.tmpl', 'w') as output:
        output.write(text)



def main():
    create_template("title", "category", "description", "link", "category" , "description", "title", "link")
    feed = feedparser.parse('composite.xml')
    jsontext = render_template(feed.entries, 'template.tmpl')
    jsontext = parse_out_html_tags(jsontext)
    jsontext = quotes(jsontext)
    jsontext = jsontext[0:jsontext.rfind(',')] + jsontext[jsontext.rfind(',') + 1:] #getting rid of extra comma at end
    jsontext = jsontext.replace("\\", "\\\\")
    #jsontext = jsontext.replace('\\x', '&#92;')
    jsontext = jsontext.replace('\\\\n', '\\n')
    jsontext = jsontext.replace('\\\\t', '\\t')
    jsontext = urlsource(jsontext, 'composite.xml')
    jsontext = decode_html_entities(jsontext)
    jsontext = quotes(jsontext)
    
    with open('news.json', 'w') as output:
        output.write(jsontext)

if __name__ == '__main__':
    main()