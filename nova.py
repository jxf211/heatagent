# -*- coding:utf-8 -*-

import logging
from keystone import get_nova_endpoint
from keystone import get_admin_tenant
from http import req_get, req_post, req_delete
import json
from novaclient.v1_1 import client
from oslo.config import cfg
from const import HTTP_CHECK_OK

log = logging.getLogger(__name__)
conf = cfg.CONF

def _get_url():
    url = None
    endpoint = get_nova_endpoint()
    admin_tenant_id = get_admin_tenant()
    if endpoint and admin_tenant_id:
        url = (endpoint % {'tenant_id': admin_tenant_id})
    return url


def get_vms():
    try:
        url = _get_url()
        if url is not None:
            resp = req_get(_get_url() + '/servers/detail?all_tenants=true')
        else:
            raise Exception('Get nova url failed')

        vms = []
        if 'servers' in resp:
            for vm_info in resp['servers']:
                vm = {}
                if 'id' in vm_info:
                    vm['id'] = vm_info['id']
                else:
                    log.error('No id in server respone')
                    continue
                if 'name' in vm_info:
                    vm['name'] = vm_info['name']
                else:
                    log.error('No name in server respone')
                    continue
                if 'OS-EXT-SRV-ATTR:instance_name' in vm_info:
                    vm['label'] = vm_info['OS-EXT-SRV-ATTR:instance_name']
                else:
                    log.error('No instance_name in server respone')
                    continue
                if 'status' in vm_info:
                    vm['state'] = vm_info['status']
                else:
                    log.error('No status in server respone')
                    continue
                if 'OS-EXT-SRV-ATTR:hypervisor_hostname' in vm_info:
                    vm['launch_server'] = \
                        vm_info['OS-EXT-SRV-ATTR:hypervisor_hostname']
                else:
                    log.error('No hypervisor_hostname in server respone')
                    continue
                if 'tenant_id' in vm_info:
                    vm['tenant_id'] = vm_info['tenant_id']
                else:
                    log.error('No tenant_id in server respone')
                    continue
                vms.append(vm)

        return vms

    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

def get_all_hosts():
    return req_get(_get_url() + '/os-hypervisors')

def get_host_detail_by_id(id=1):
    return req_get(_get_url() + '/os-hypervisors/%s' % id)

def get_flavors():
    try:
        url = _get_url()
        if url is not None:
            code, resp = req_get(url + '/flavors')
        else:
            raise Exception('Get nova url failed')

        return code, resp
    except Exception as e:
        log.error(e)
        raise Exception

def create_vm(json_data):
    """
    **Request Example**:
        json_data={
                    "server": {
                        "name":"test_vm_7.21",
                        "imageRef":"d578f69c-9071-4df9-867e-d875a0a9bdb9",
                        "flavorRef":2,
                        "max_count": 1,
                        "min_count": 1,
                        "networks":[{"uuid":"08aa8aa3-2e9e-4fcc-87fa-ea5ccbf8dde2"}]
                        }
                  }   
    """
    try: 
        url = _get_url()
        if url is not None:
            code, resp = req_post(url +'/servers', json_data)
        else:
            raise Exception('Get nova url failed')
        return code, resp
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

def delete_vm(vmuuid):
    try:
        url = _get_url()
        if url is not None:
            url += '/servers/'+ vmuuid
            code, resp = req_delete(url)
        else:
            raise Exception('Get nova url failed')
        return code, resp
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

def get_vmdata(vm_uuid):
    try:
        url = _get_url()
        if url is not None:
            url += '/servers/'+ vm_uuid
            code, resp = req_get(url)
        else:
            raise Exception('Get nova url failed')
        vmdata={}      
        if code in HTTP_CHECK_OK and "server" in resp:
            for  key, value in resp["server"].iteritems():
                if key == "addresses":
                    vmdata[key] = value
                if key == "image":
                    vmdata[key] = value
                if key == "name":
                    vmdata[key] = value

        return code, vmdata
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

