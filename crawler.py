#python 3

import html_link_parser as lp
import url_handler as url_h
import ip_geolocator
import traceroute_v2 as trc
#import time
#import multiprocessing
import socket
import re

import urllib
import time 
import datetime, threading
import subprocess

"""
                                Basic Web Crawler. 

        Searches for all links/subfolders with start_url prefix connected by the web.

"""

"""
    Node


    should produce a tree structure, where the root is the first url passed, with list of desendent nodes, 


        node:
                parent_ip
                url_object
                children [url_objects]
"""

#tmp global
unique_urls = []
def add_to_unique_url_list(url):
    if url not in unique_urls:  unique_urls.append(url)

#tmp global
unique_ips = []
def add_to_unique_ip_list(ip, url):
    if ip not in unique_ips:
        l = []
        l.append(ip)
        l.append(url)
        unique_ips.append(l)

class Web_Node( object ):

    def spawn(self):
        children = []

        for l in self.url_object.links:
            #   ***TMP***                                                 tmp global  (2)
            global num_crawlers
            num_crawlers = num_crawlers + 1
            if num_crawlers < max_children:
                print ("num crawlers : %d " % num_crawlers)
                c = Web_Node( l, self.url_object.ip )
                children.append(c)

                #add to unique urls list
                add_to_unique_url_list(l)

                #add to unique urls list
                add_to_unique_ip_list(get_ip_from_domain(l), l)

        return children


    def __init__(self, url, parent_ip):

        parser = lp.Link_Parser()

        self.parent_ip = parent_ip
        self.url_object = url_h.URL_Handler(url)

        #   ***TMP***                                                 tmp global  (2)
        global parents
        parents = parents + 1
        if parents < parent_cap:
            print ("parents : %d " % parents)
            self.children = self.spawn()

def write(txt,name):
    """ write vector v to a file name.txt in jupyter notebooks vector format """
    f = open(name, 'w')
    f.write(" %s " % txt)

def write_vector(v,name):
    """ write vector v to a file name.txt in jupyter notebooks vector format """
    f = open(name, 'w')
    for i in v: f.write(" %s " % i)

def strip_url(url):
    """ remove past www. for socket getaddrinfo format """

    try :
        regex = r'(http://)?(www\.)?(?P<target>.*?)/'
        match_obj = re.match(regex, url)
        stripped_url = match_obj.group('target')
    except:
        stripped_url = "-1"
    return stripped_url

def get_ip_from_domain(domain_name):
        """ passing domain name should return ip address """
        stripped_url = strip_url(domain_name)
        ip = "-1"

        try:
            host_info = socket.getaddrinfo(stripped_url,None, proto=socket.IPPROTO_TCP)
            ip = host_info[0][4][0]
        except: print ("file:crawler.py\nfunc:get_ip_from_domain")

        return ip

class ip_obj( object ):

    def to_json_string(self):
        json_dict = {}

        json_dict["url"] = self.url
        json_dict["ip"] = self.ip
        json_dict["location"] =  self.location.to_json_string()  #a json dict

        return json_dict

    def __init__(self, url):
        self.url = url
        self.ip = get_ip_from_domain(url)
        self.location = ip_geolocator.Location(self.ip)

class www_unique_urls(object):

    def to_json_string(self):
        json_dict = {}
        json_dict["urls"] = self.urls
        return json_dict

    def add_ip_obj(self, ip_obj):
        self.urls.append(ip_obj.to_json_string())

    def __init__(self):
        self.urls = []


def extract_ip(trace_route_line):
    try:
        s = trace_route_line.split('(')
        s= s[1].split(')')
        ip = s[0]
    except:
        print ("f:crawler.py\nf():extract_ip\n\terror extracting ip from traceroute line")
        ip = "-1"
    return ip

"""
    add timeout for tace
"""
def trace(hostname):
    """ use system trace route and return list of unique ips """

    #unique ips
    unique_ips = []

    #modify hostname to correct format
    hostname = strip_url(hostname)

    #stop ip
    host_ip = get_ip_from_domain(hostname)
    unique_ips.append(host_ip)

    hops = 0
    max_hops = 30

    timeout = time.time() + 10   # 10 seconds
    traceroute = subprocess.Popen(["traceroute", '-w', '100', hostname],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while (True):
            hop = str(traceroute.stdout.readline())

            if not hop: break

            ip = extract_ip(str(hop))

            print(str(hop))
            print(ip)

            if ip not in unique_ips:
                unique_ips.append(ip)

            if ip == host_ip: break
            if hops >= max_hops: break
            if time.time() > timeout: break

            hops += 1
    return unique_ips

"""
                                #--------------------------*
                                #      start program       *
                                #--------------------------*
"""

start_url = "http://www.smu.edu"
start_ip = get_ip_from_domain(start_url)

#   ***TMP***                                                           tmp global (1)
num_crawlers = 0
max_children = 1000
parents = 0
parent_cap = 2

#create tree
web_root = Web_Node( start_url, start_ip )



"""
    after collecting urls write all materials to file
"""

print ("succsessful collection of urls\nnumber of unique urls collected : %d" % (len(unique_urls)))

www = www_unique_urls()
for url in unique_urls:
    endpoint_obj = ip_obj(url)
    www.add_ip_obj(endpoint_obj)

write(www.to_json_string(), "www.txt")
write_vector(unique_ips, "unique_ips.txt")
print (www.to_json_string())


"""
    run traceroute on unique ips colleted and write results to a file
"""
traceroutes = []
for ip in unique_ips:
    print ("running traceroute on domain: %s, \t ip: %s" % (ip[1], ip[0]))
    traceroutes += trace(ip[1])

write_vector(traceroutes, "traceroute_ips.txt")
print (traceroutes)


