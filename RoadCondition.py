# -*- coding: utf-8-*-
import sys
import os
import logging
import json, urllib
from urllib import urlencode

WORDS = ["LUKUANG"]
SLUG = "roadcondition"

def request(url, params):    

    f = urllib.urlopen("%s?%s" % (url, params))

    content = f.read()
    return json.loads(content)


def handle(text, mic, profile, wxbot=None):
    logger = logging.getLogger(__name__)
    
    if SLUG not in profile or \
       'app_key' not in profile[SLUG]:
        mic.say(u"插件配置有误，插件使用失败")
        return
        
    app_key = profile[SLUG]['app_key']  

    mic.say(u'哪条道路')
    input = mic.activeListen(MUSIC=True)
    if input is None:
        mic.say(u'已取消')
        return
    
  
    url_transit = "http://restapi.amap.com/v3/traffic/status/road"
   
    citycode = u"&adcode=440300&key="+app_key
    params_condition = "name="+input + citycode 
   
    res = request(url_transit,params_condition.encode("utf-8"))
    print res
    if res:        
        status = res["status"]
        if status == "1":
            print "status == 1"
            print res['trafficinfo']
            if len(res['trafficinfo']) > 0:
                place_name = res['trafficinfo']['evaluation']['description']
                place_name1 = res['trafficinfo']['description']
                mic.say(place_name)
                mic.say(place_name1)                
            else:
                mic.say(u"错误的位置")
                return
        else:
            logger.error(u"位置接口:" + res['message'])
            return
    else:
        logger.error(u"位置接口调用失败")
        return 


def isValid(text):
    return any(word in text for word in [u"路况", u"上班", u"塞车"])
