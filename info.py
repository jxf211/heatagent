# -*- coding:utf-8 -*-

import logging
import json
from const import HTTP_OK, HTTP_INTERNAL_SERVER_ERROR
from keystone import get_tenants
from nova import get_vms
from neutron import get_ports
from neutron import get_networks
from neutron import get_subnets
from neutron import get_routers
from glance import get_images
from nova import get_flavors, create_vm, delete_vm
from neutron import create_network, delete_network, create_subnet,\
delete_subnet, create_port, delete_port
from heat import create_stack, get_stack_status,\
delete_stack,get_stack_resource

log = logging.getLogger(__name__)

nova_uri = None
neutron_uri = None


def info_request(method=None, headers=None,
                 params=None, body=None, **kwargs):
    info = {}
    try:
        #networks = get_networks()
        #info['networks'] = networks
        #subnets = get_subnets()
        #info['subnets'] = subnets
        #vms = get_vms()
        #info['vms'] = vms
        #ports = get_ports()
        #info['ports'] = ports
        #tenants = get_tenants()
        #info['tenants'] = tenants
        #routers = get_routers()
        #info['routers'] = routers
        images = get_images()
        info['images'] = images
        flavors = get_flavors()
        info['flavors'] = flavors
        return HTTP_OK, json.dumps(info)
    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)

def info_images(method=None, headers=None,
                params=None, body=None, **kwargs):
    try:
        code, images = get_images()
        return code, json.dumps(images)
    
    except Exception as e:
	    return HTTP_INTERNAL_SERVER_ERROR, str(e)

def info_flavors(method=None, headers=None,
                 params=None, body=None, **kwargs):
    try:
	    code, flavors = get_flavors()
	    return code, json.dumps(flavors)

    except Exception as e:
	    return HTTP_INTERNAL_SERVER_ERROR, str(e)
          
def info_create_vm(method=None, headers=None,
                   params=None, body=None, **kwargs):
    try:
        log.info("start create_vm")
        code, resp = create_vm(body)
        return code, json.dumps(resp)
        
    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)
         
def info_delete_vm(method=None, headers=None,
                   params=None, body=None, vmuuid=None, **kwargs):
    try:
        code, resp = delete_vm(vmuuid)
        return code, json.dumps(resp)

    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)
        
def info_create_network(method=None, headers=None,
                        params=None, body=None, **kwargs):
    try:
        code, resp = create_network(body)
        return code, json.dumps(resp)
    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)

def info_delete_network(method=None, headers=None,
                        params=None, body=None, network_uuid=None, **kwargs):
    try:
        code, resp = delete_network(network_uuid)
        return code, json.dumps(resp)
    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)

def info_create_subnet(method=None, headers=None,
                       params=None, body=None, **kwargs):
    try:
        code, resp = create_subnet(body)
        return code, json.dumps(resp)
    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)

def info_delete_subnet(method=None, headers=None,
                       params=None, body=None, subnet_uuid=None, **kwargs):
    try:
        code, resp = delete_subnet(subnet_uuid)
        return code, json.dumps(resp)
    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)

def info_create_port(method=None, headers=None,
                     params=None, body=None, **kwargs):
    try:
        code, resp = create_port(body)
        return code, json.dumps(resp)
    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)

def info_delete_port(method=None, headers=None,
                     params=None, body=None, port_uuid=None, **kwargs):
    try:
        code, resp = delete_port(port_uuid)
        return code, json.dumps(resp)
    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)
 
def info_create_stack(method=None, headers=None,
                      params=None, body=None, **kwargs):
    try:
        code, resp = create_stack(body)
        return code, json.dumps(resp)
    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)

def info_get_stack(method=None, headers=None,
                   params=None, body=None,stack_name=None, **kwargs):
    try:
        code, resp = get_stack_status(stack_name)
        return code, json.dumps(resp) 
    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)

def info_delete_stack(method=None, headers=None,
                      params=None, body=None,stack_name=None, **kwargs):
    try:
        code, resp = delete_stack(stack_name)
        return code, json.dumps(resp) 
    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)

def info_get_stackres(method=None, headers=None,
                      params=None, body=None,stack_name=None, **kwargs):
    try:
        code, resp = get_stack_resource(stack_name)
        return code, json.dumps(resp)
    except Exception as e:
        return HTTP_INTERNAL_SERVER_ERROR, str(e)            
