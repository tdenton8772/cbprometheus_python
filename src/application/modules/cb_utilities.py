import urllib2
import json

import re
from random import shuffle

class Error(Exception):
   """Base class for other exceptions"""
   pass

class SeedNodeDown(Error):
   """Raised when all the seed nodes are down"""
   pass

def snake_caseify(input_str):
    '''converts to snake case'''
    converted_str = '_'.join(filter(None, re.split("([A-Z][^A-Z]*)", input_str))).lower()
    return converted_str

def basic_authorization(user, password):
    '''Doc String'''
    s = user + ":" + password
    return "Basic " + s.encode("base64").rstrip()

def str2bool(v):
    '''Converts string values to boolean'''
    return v.lower() in ("yes", "true", "t", "1")

def value_to_string(ip_address):
    '''converts IP addresses and other values to strings without special characters'''
    ip_address = ip_address.split(":")[0].replace(".", "_").replace("+", "_")
    return ip_address

def rest_request(auth, url):
    _url = url
    req = urllib2.Request(_url,
                          headers={
                              "Authorization": auth,
                              "Content-Type": "application/x-www-form-urlencoded",

                              # Some extra headers for fun
                              "Accept": "*/*",  # curl does this
                              "User-Agent": "check_version/1",
                          })

    f = (urllib2.urlopen(req, timeout=1)).read()
    result = json.loads(f)
    return result

def check_cluster(url, username, pw):
    urls = url.split(",")
    shuffle(urls)
    print(urls)
    active = False
    auth = basic_authorization(username, pw)
    for _url in urls:
        try:
            rest_request(auth, "http://{}:8091/pools/default".format(_url))
            url = _url
            active = True
            break
        except:
            pass
    if active == False:
        raise SeedNodeDown
    else:
        return url
