# -*- coding:utf-8 -*-

import logging
from keystone import get_glance_endpoint
from http import req_get

def _get_url():
   url = get_glance_endpoint()
   return url

def get_images():
    try:
	    url = _get_url()
	    if url is not None:
	      code, resp = req_get(url + '/v2/images')
	    else:
	        raise Exception('Get glance url failed')

	    return code, resp
    except Exception as e:
	    log.err(e)
	    raise Exception('Error: %s' % e)	
