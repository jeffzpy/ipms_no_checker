#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Chorus HTTP&HTTPS Authentication module generates Proxy string to simplify Chorus Proxy Authenticaion access \r\n
    To get this module generating right proxy string to cross chorus proxy, you will need type correct chorus LAN user name and
    password when calling function <generate_proxy_str>
"""

__author__      = "Jeff Z: Jeff Zhang@Chorus.co.nz"
__copyright__   = "​​Owned and Maintained by Chorus NZ"

#import global settings
import config as cfg

#Proxy Setting:
__proxy_ip = cfg.proxy_ip
__proxy_port = cfg.proxy_port
__domain_str = cfg.proxy_domain_str

def generate_proxy_str(usernm,passwd):
    if (usernm == '') or (passwd == ''):
        return 'err: Empty Username or Password'
    proxy_str = ''.join(['http://',__domain_str,'\\',usernm,':',passwd,'@',__proxy_ip,':',__proxy_port])
    proxyDict = {'http' : proxy_str, 
                 'https' : proxy_str}
    return proxyDict