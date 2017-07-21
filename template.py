from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from bs4 import BeautifulSoup

class template_model():
    def __init__(self, event_name, start_info, location, event_url, end_info, description, tags, pic_url):
        self.event_name = event_name
        self.start_info = start_info
        self.location = location
        self.event_url = event_url
        self.end_info = end_info
        self.description = description
        self.tags = tags
        self.pic_url = pic_url
    
        self.template_model = ""
        
        if self.end_info == "":
            #end_info = one hour greater than start_info
            pass
        
    def create_template_model(self):

        text = """"feed":
[
    {% for entry in feed %}
    {
        "weburl": "",
        "evtname": "{{entry."""+self.event_name+"""}}",
        "url": "{{ entry.""" + self.event_url + """}}",
        "location": "{{ entry.""" + self.location + """}}",
        "evtsource": "{{ entry.""" + self.event + """}}",
        "createdate": "",
        "evtdesc": "{{ entry.""" + self.description + """}}",
        "grps": ["{{ entry.""" + tags + """}}"],
        "endtime": "{{ entry.""" + end_info + """}}",
        "picurl": "{{ entry.""" + pic_url + """}}",
        "starttime": "{{ entry.""" + start_info + """}}"
    },
    {% endfor %}
]
"""
        
        return
    
    def return_template(self):
        return
        
    def render_template(self, data, template_name, filters=None):
        """Render data using a jinja2 template"""
        env = Environment(loader=FileSystemLoader(''))
    
        if filters is not None:
            for key, value in filters.iteritems():
                env.filters[key] = value
    
        template = env.get_template(template_name)
        return template.render(feed=data).encode('utf-8')
    
    def parse_out_html_tags(self,string):
        toclean = re.compile('<.*?>')
        cleantext = re.sub(toclean, '',string)
        return cleantext
    
    def decode_html_entities(self, string):
        decodedtext = BeautifulSoup(string)
        return decodedtext.text.encode('utf-8')
    
    def create_template(self, event_name, start_info, location, event_url, end_info="", description="", tags="", pic_url=""):
        """create .tmpl file to be used in main()
        required fields: event_name, start_info, location, event_url
        optional fields: end_info, description, tags, pic_url
        """
        # args = [event_name, start_info, location, event_url, end_info, description, tags, pic_url]
    
        # for item in args:
            
    
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
    