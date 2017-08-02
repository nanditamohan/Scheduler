#Copyright Jon Berg , turtlemeat.com

import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pri
from rss2json import *

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith(".html"):
                f = open(curdir + sep + self.path) #self.path has /test.html
#note that this potentially makes every file on your computer readable by the internet

                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            if self.path.endswith(".esp"):   #our dynamic content
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write("hey, today is the" + str(time.localtime()[7]))
                self.wfile.write(" day in the year " + str(time.localtime()[0]))
                return

            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


    def do_POST(self):
        global rootnode
        try:
            print 1
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # if ctype == 'multipart/form-data':
            query=cgi.parse_multipart(self.rfile, pdict)
            RSSlink = query.get('RSSlink')[0]
            name = query.get('name')[0]
            start = query.get('start')[0]
            location = query.get('location')[0]
            eventurl = query.get('eventurl')[0]
            end = query.get('end')[0]
            piclink = query.get('piclink')[0]
            tag = query.get('tag')[0]
            description = query.get('description')[0]

            create_template(name, start, location, eventurl, end , description, tag, piclink)
            feed = feedparser.parse(RSSlink)
            jsontext = render_template(feed.entries, 'template.tmpl')
            jsontext = parse_out_html_tags(jsontext)
            jsontext = quotes(jsontext)
            jsontext = jsontext[0:jsontext.rfind(',')] + jsontext[jsontext.rfind(',') + 1:] #getting rid of extra comma at end
            jsontext = jsontext.replace('\\x', '\\u00')
            
            jsontext = urlsource(jsontext, RSSlink)
            jsontext = decode_html_entities(jsontext)
            jsontext = quotes(jsontext)

            self.send_response(301)

            self.end_headers()

            with open('news.json', 'w') as output:
                output.write(jsontext)

            self.wfile.write("<HTML>Parsed<BR><BR>");
            self.wfile.write(jsontext);

        except Exception as e:
            print e
            pass


def main():
    try:
        server = HTTPServer(('', 8012), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
