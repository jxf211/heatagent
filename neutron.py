# -*- coding:utf-8 -*-

import logging
from keystone import get_neutron_endpoint
from http import req_get, req_post, req_delete
import json
log = logging.getLogger(__name__)


def _get_url():
    url = get_neutron_endpoint()
    return url


def get_ports():
    try:
        url = _get_url()
        if url is not None:
            resp = req_get(url + '/v2.0/ports')
        else:
            raise Exception('Get neutron url failed')

        ports = []
        if 'ports' in resp:
            for port_info in resp['ports']:
                port = {}
                if ('device_owner' in port_info and
                    port_info['device_owner'] == 'network:dhcp'):
                    # skip dhcp port
                    continue
                if 'id' in port_info:
                    port['id'] = port_info['id']
                else:
                    log.error('No id in port respone')
                    continue
                if 'mac_address' in port_info:
                    port['mac_address'] = port_info['mac_address']
                else:
                    log.error('No mac_address in port respone')
                    continue
                if 'fixed_ips' in port_info:
                    port['fixed_ips'] = []
                    for fixed_ip in port_info['fixed_ips']:
                        if ('subnet_id' in fixed_ip and
                                'ip_address' in fixed_ip):
                            port['fixed_ips'].append(
                                {'subnet_id': fixed_ip['subnet_id'],
                                 'ip_address': fixed_ip['ip_address']})
                else:
                    log.error('No fixed_ips in port respone')
                    continue
                if 'network_id' in port_info:
                    port['network_id'] = port_info['network_id']
                else:
                    log.error('No network_id in port respone')
                    continue
                if 'tenant_id' in port_info:
                    port['tenant_id'] = port_info['tenant_id']
                else:
                    log.error('No tenant_id in port respone')
                    continue
                if 'device_id' in port_info:
                    port['device_id'] = port_info['device_id']
                else:
                    log.error('No device_id in port respone')
                    continue
                ports.append(port)

        return ports

    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)


def get_networks():
    try:
        url = _get_url()
        if url is not None:
            resp = req_get(url + '/v2.0/networks')
        else:
            raise Exception('Get neutron url failed')

        networks = []
        if 'networks' in resp:
            for nw_info in resp['networks']:
                network = {}
                if 'id' in nw_info:
                    network['id'] = nw_info['id']
                else:
                    log.error('No id in network respone')
                    continue
                if 'name' in nw_info:
                    network['name'] = nw_info['name']
                else:
                    log.error('No name in network respone')
                    continue
                if 'provider:segmentation_id' in nw_info:
                    network['segmentation_id'] = \
                        nw_info['provider:segmentation_id']
                else:
                    log.error('No segmentation_id in network respone')
                    continue
                if 'tenant_id' in nw_info:
                    network['tenant_id'] = nw_info['tenant_id']
                else:
                    log.error('No tenant_id in network respone')
                    continue
                if 'shared' in nw_info:
                    network['shared'] = nw_info['shared']
                else:
                    log.error('No shared info in network respone')
                    continue
                if 'router:external' in nw_info:
                    network['external'] = nw_info['router:external']
                else:
                    log.error('No router:external in network respone')
                    continue
                networks.append(network)

        return networks

    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)


def get_subnets():
    try:
        url = _get_url()
        if url is not None:
            resp = req_get(url + '/v2.0/subnets')
        else:
            raise Exception('Get neutron url failed')

        subnets = []
        if 'subnets' in resp:
            for sub_info in resp['subnets']:
                subnet = {}
                if 'id' in sub_info:
                    subnet['id'] = sub_info['id']
                else:
                    log.error('No id in subnet respone')
                    continue
                if 'cidr' in sub_info:
                    subnet['cidr'] = sub_info['cidr']
                else:
                    log.error('No cidr in subnet respone')
                    continue
                if 'network_id' in sub_info:
                    subnet['network_id'] = sub_info['network_id']
                else:
                    log.error('No network_id in subnet respone')
                    continue
                if 'tenant_id' in sub_info:
                    subnet['tenant_id'] = sub_info['tenant_id']
                else:
                    log.error('No tenant_id in subnet respone')
                    continue
                if 'gateway_ip' in sub_info:
                    subnet['gateway_ip'] = sub_info['gateway_ip']

                subnets.append(subnet)

        return subnets

    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

def get_routers():
    try:
        url = _get_url()
        if url is not None:
            resp = req_get(url + '/v2.0/routers')
        else:
            raise Exception('Get neutron url failed')
        routers = []
        if 'routers' in resp:
            for router_q in resp['routers']:
                router = {}
                router['name'] = router_q['name']
                router['tenant_id'] = router_q['tenant_id']
                router['id'] = router_q['id']
                routers.append(router)
        return routers
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % str(e))

def create_network(json_data):
    try:
        url = _get_url()
        if url is not None:
           code, resp = req_post(url + '/v2.0/networks', json_data)
        else:
            raise Exception('Get neutron url failed')
        return code, resp
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

def delete_network(network_uuid):
    try:
        url = _get_url()
        if url is not None:
           code, resp = req_delete(url + '/v2.0/networks/' + network_uuid)
        else:
            raise Exception('Get neutron url failed')
        
        return code, resp
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

def create_subnet(json_data):
    """
    **Request Example**:
    subnet = {
                "subnet":{
                    "network_id":"08aa8aa3-2e9e-4fcc-87fa-ea5ccbf8dde2",
                    "ip_version": 4,
                    "cidr":"10.10.40.0/24",
                    "name":"testsubnet",   
                     }
            }
    """
    try:
        url = _get_url()
        if url is not None:
           code, resp = req_post(url + '/v2.0/subnets/', json_data)
        else:
            raise Exception('Get neutron url failed')
        return code, resp
    except Exception as e:
        log.error(e)

def delete_subnet(subnet_uuid):
    try:
        url = _get_url()
        if url is not None:
           code, resp = req_delete(url + '/v2.0/subnets/' + subnet_uuid)
        else:
            raise Exception('Get neutron url failed')
        
        return code, resp
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

def create_port(json_data):
    """
    port = {
            "port":{
                "network_id":"08aa8aa3-2e9e-4fcc-87fa-ea5ccbf8dde2",
                "name": "private-port",
                "admin_state_up": "true"
                }
        }
    """
    try:
        url = _get_url()
        if url is not None:
            code, resp = req_post(url + '/v2.0/ports.json', json_data)
        else:
            raise Exception('Get neutron url failed')

        return code, resp
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)

def delete_port(pord_uuid):
    try:
        url = _get_url()
        if url is not None:
            code, resp = req_delete(url + '/v2.0/ports/' + pord_uuid + '.json')
        else: 
            raise  Exception('Get neutron url failed')
        return code, resp
    except Exception as e:
        log.error(e)
        raise Exception('Error: %s' % e)
        
