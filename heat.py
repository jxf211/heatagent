# -*- coding:utf-8 -*-

import logging
from keystone import get_glance_endpoint, get_heat_endpoint
from http import req_get, req_post, req_delete
from keystone import get_admin_tenant
import json
from oslo.config import cfg
from const import HTTP_CHECK_OK,HTTP_INTERNAL_SERVER_ERROR,HTTP_OK_NORESP
from nova import get_vmdata
import time
log = logging.getLogger(__name__)
logging.basicConfig()
conf = cfg.CONF

heat_opts = [ 
    cfg.StrOpt("subnet_cidr", default = '10.20.30.0/24',
                    help=" The vm ip to use"),
    cfg.StrOpt("vm_flavor", default = "m1.small",
                    help = "Create vm flavor"),
    cfg.StrOpt("publicnet_id", default = "047404b0-295e-4f2f-be15-7644c0d79e7b",
                    help = "public network id")
    ]
conf.register_opts(heat_opts, group="heat")

def _get_url():
    url = None
    endpoint = get_heat_endpoint()
    admin_tenant_id = get_admin_tenant()
    if endpoint and admin_tenant_id:
        url = (endpoint % {'tenant_id': admin_tenant_id})
    return url

def get_stack_href_url(resdata):
    try:
        url_data = resdata["stack"]["links"]
        for info in url_data:
            if isinstance(info, dict):
                return  info.get("href", None)
      
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)
        
def create_stack(json_data):
    try:
        url = _get_url()
        if url is not None:
            stack_data = convert_jsondata_to_heat_template(json.loads(json_data))
            #stack_data = json_data
            code, resp = req_post(url + '/stacks', stack_data)
        else:
            raise Exception('Get heat url failed')

        if code in HTTP_CHECK_OK or \
            code in HTTP_OK_NORESP:
            while True:
                if not resp:
                    break
                call_url = get_stack_href_url(resp)
                if call_url is None:
                    break
                code, resp = req_get(call_url) 
                if code not in HTTP_CHECK_OK  or "stack" not in resp:
                    break
                stack_resp = resp["stack"]
                if "stack_status"  in stack_resp and \
                    stack_resp["stack_status"] != "CREATE_IN_PROGRESS" and \
                    stack_resp["stack_status"] != "ROLLBACK_IN_PROGRESS":
                    if stack_resp["stack_status"] == "ROLLBACK_COMPLETE":
                        code =  HTTP_INTERNAL_SERVER_ERROR
                    break
                time.sleep(2)

        return code, resp
    except Exception as e:
       log.error(e)
       raise Exception('Error: %s' % e)

def convert_jsondata_to_heat_template(data):
    try:
        stackdata={}
        stackdata["disable_rollback"] = "false"
        
        if "name" in data:
            stackdata["stack_name"] = data.get("name", None)
        else:
            log.error("stack name is null")
            return
        template = {}
        stackdata["template"] = template
        template["heat_template_version"] = "2013-05-23"
        template["description"] = "Simple template to test heat commands"
       
        resources = {}
        template["resources"] = resources
        resources["private_net"] = {
            "type":"OS::Neutron::Net",
            "properties":{
                "name":"private_net",
                }
            }
        resources["private_subnet"] = {
            "type":"OS::Neutron::Subnet",
            "properties":{
                "name":"private_subnet",
                "network_id":{"Ref":"private_net"},
                "cidr":conf.heat.subnet_cidr,
                "dns_nameservers":["114.114.114.114"]
                }
            }

        if "images" in data:
            image_data = data["images"]
        else:
            log.error("image is null")
            return
        vmcount = 1    
        for image in image_data:
            if "id" in image:
                if "name" in image:
                    image_name = image["name"]
                else:
                    image_name = "testvm" + str(vmcount)
                if "flavor" in image:
                    image_flavor = image["flavor"]
                else :
                    image_flavor = conf.heat.vm_flavor 
                resources[image_name] = {
                    "type": "OS::Nova::Server",
                    "properties": {
                        "flavor": image_flavor,
                        "image": image["id"],
                        "networks":[{"network":{"Ref":"private_net"}}]
                        }    
                    }
                if "isp" in image:
                    if "router" not in resources:
                       resources["router"] = {
                            "type":"OS::Neutron::Router",
                            "properties":{\
                                "external_gateway_info":{"network":conf.heat.publicnet_id}
                            }
                        }
                    if "router_interface" not in resources:
                        resources["router_interface"] = {
                            "type":"OS::Neutron::RouterInterface",
                            "properties":{
                                "router_id":{"Ref":"router"},
                                "subnet_id":{"Ref":"private_subnet"}
                                }
                            }
                    resources["server_port"+str(vmcount)] = {
                        "type": "OS::Neutron::Port",
                        "properties":{
                            "network_id":{"Ref":"private_net"},
                            "fixed_ips":[{"subnet_id":{"Ref":"private_subnet"}}]
                            }
                        }
                    resources["server_floating_ip"+str(vmcount)] = {
                        "type":"OS::Neutron::FloatingIP",
                        "properties":{
                            "floating_network_id": conf.heat.publicnet_id,
                            "port_id":{"Ref":"server_port"+str(vmcount)}
                            }
                        }
                    
                    resources[image_name]["properties"]["networks"]=[{"port":{"Ref":"server_port"+str(vmcount)}}]
            vmcount += 1
        return json.dumps(stackdata)
                      
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

def get_stack_status(stack_name):
    try:
        url = _get_url()
        if url is not None:
            code, resp = req_get(url + '/stacks/'+ stack_name)
        else:
            raise Exception("Get heat url failed")

        return code, resp
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

def delete_stack(stack_name):
    try:
        stack_id = _get_stackid_by_stackname(stack_name)
        if stack_id is not None:
            url = _get_url()
            if url is not None:
                code, resp = req_delete(url + '/stacks/'+ stack_name + '/' +\
                                        stack_id)
            else:
                raise Exception("Get heat url failed")
        else:
            raise Exception("Get stack id failed or stack null")
        return code, resp
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

def _get_stackid_by_stackname(stack_name):
    stack_id = None
    url = _get_url()
    if url is not None:
        code, resp = req_get(url + '/stacks/'+ stack_name)
        if "stack" in resp and "id" in resp["stack"]:
            stack_id = resp["stack"]["id"]
    else:
        raise Exception("Get heat url failed")
    return stack_id

def get_stack_resource(stack_name):
    try:
        log.debug("get stack info")
        code, resp = _get_vminfo_by_stackname(stack_name)
        return code, resp
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

def _get_vminfo_by_stackname(stack_name):
    try:
        url = _get_url()
        if url is not None:
            code, resp = req_get(url + '/stacks/'+ stack_name + '/resources')
        else:
            raise Exception("Get heat url failed")
        vmdata={}
        if code in HTTP_CHECK_OK:
            if resp:
                vmdata = _get_vm_by_stackinfo(resp)
        else:
            return code, resp

        return code, vmdata
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e) 

def _get_vm_by_stackinfo(data):
    vmdata={}
    if "resources" in data:
        vmdata["vms"] = []
        for infodata in data["resources"]:
            if "resource_type" in infodata and \
                infodata["resource_type"] == "OS::Nova::Server" and \
                "physical_resource_id" in infodata:
                vm_id = infodata["physical_resource_id"]
                code, resp = get_vmdata(vm_id)
                if code in HTTP_CHECK_OK:
                    vmdata["vms"].append(resp) 
                else:
                    log.error("get vmdata faild vmid:%s", vm_id)
    return vmdata
                 
