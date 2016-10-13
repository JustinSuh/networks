#python 3

from html.parser import HTMLParser  
#from urllib.request import urlopen  
from urllib import parse
import urllib

"""

    HTML parser extension, Link Parser Class

    use:
            #include html_link_parser

            parser = Link_Parser()
            links = parser.get_links(url)

"""
class Link_Parser( HTMLParser ):

    def get_links(self, url):

        """ getLinks method: takes url reutrns list of urls found in html """
        
        self.urls = []
        self.url_base = url

        """
                REQUEST MADE HERE
        """

        opener = urllib.request.URLopener() #default (proxies=None)
        opener.version = "Chrome/53.0.2785.116" #version Python-urllib/3.5 gets 999

        print ("file:html_link_parser.py \nf():get_links \n\turl request:\t%s" % url)
        try:
            response = opener.open(url) #request, "get" by defualt 
            if response.getheader('Content-Type')=='text/html; charset=utf-8':
                htmlBytes = response.read()
                htmlString = htmlBytes.decode("utf-8")
                self.feed(htmlString) #calls parser
                print("\tsucsessful retrieval.\n")
        except Exception as e: 
            print("\trequest error: %s\n" % e)

        return self.urls

    def handle_starttag(self, tag, attrs):

        """ impliment starttag method from HTMLParser to search for urls"""
        
        if tag == 'a':
            for (attr, url) in attrs:
                if attr == 'href':
                    #new_url = self.url_base + url
                    new_url = parse.urljoin(self.url_base, url)
                    self.urls = self.urls + [new_url]

