# -*- coding:utf-8 -*-

import webob
import webob.dec
import logging
from const import HTTP_OK
from host import host_request
from info import info_request, info_images, info_flavors, info_create_vm,\
info_delete_vm, info_create_network, info_delete_network,info_create_network,\
info_create_subnet, info_delete_subnet, info_create_port, info_delete_port,\
info_create_stack, info_get_stack, info_delete_stack, info_get_stackres
from webob.dec import *
from webob.exc import *
log = logging.getLogger(__name__)

def render_response(body, status):
    """
    @body  :Response的body
    @status:Response的状态码
    """
    # 获取body长度
    content_len = str(len(body))
    # 生成Response header
    headers = [('Content-type', 'application/json'),
               ('Content-length', content_len)]
    return webob.Response(body=body, status=status, headerlist=headers)


class Controller(object):
    def __init__(self):
        pass

    @webob.dec.wsgify()
    def __call__(self, req):
        kwargs = req.environ['wsgiorg.routing_args'][1]
        action = kwargs.get('action')
        if action is None:
            log.error('action is None')
            msg = '{"ERROR":"Internal Server Error"}'
            return render_response(msg, '500  ')
        method = getattr(self, action, None)
        if method is None:
            log.error('method is None')
            msg = '{"ERROR":"Internal Server Error"}'
            return render_response(msg, '500  ')
        status, msg = method(method=req.method,
                             headers=dict(req.headers),
                             params=dict(req.params),
                             body=req.body, **kwargs)

        return render_response(msg, '%d  ' % status)

    def info_api(self, method=None, headers=None,
                 params=None, body=None, **kwargs):
        return info_request(method=method, headers=headers,
                            params=params, body=body, **kwargs)

    def host_api(self, method=None, headers=None,
                 params=None, body=None, **kwargs):
        return host_request(method=method, headers=headers,
                            params=params, body=body, **kwargs)

    def get_images_api(self, method=None, headers=None,
                            params=None, body=None, **kwargs):
        return info_images(method=method, headers=headers,
                            params=params, body=body, **kwargs)

    def get_flavors_api(self, method=None, headers=None,
                         params=None, body=None, **kwargs):
        return info_flavors(method=method, headers=headers,
                            params=params, body=body, **kwargs)
    
    def create_vm_api(self, method=None, headers=None,
                       params=None, body=None, **kwargs):
        return info_create_vm(method=method, headers=headers,
                              params=params, body=body, **kwargs)

    def delete_vm_api(self, method=None, headers=None,
                      params=None, body=None, **kwargs):
        return info_delete_vm(method=method, headers=headers,
                             params=params, body=body, **kwargs)

    def create_network_api(self, method=None, headers=None,
                            params=None, body=None, **kwargs):
        return info_create_network(method=method, headers=headers,
                                params=params, body=body, **kwargs)

    def delete_network_api(self, method=None, headers=None,
                            params=None, body=None, **kwargs):
        return info_delete_network(method=method, headers=headers,
                                    params=params, body=body, **kwargs)

    def create_subnet_api(self, method=None, headers=None,
                            params=None, body=None, **kwargs):
        return info_create_subnet(method=method, headers=headers,
                                    params=params, body=body, **kwargs)

    def delete_subnet_api(self, method=None, headers=None,
                            params=None, body=None, **kwargs):
        return info_delete_subnet(method=method, headers=headers,
                                    params=params, body=body, **kwargs)

    def create_port_api(self, method=None, headers=None,
                            params=None, body=None, **kwargs):
        return info_create_port(method=method, headers=headers,
                                    params=params, body=body, **kwargs)

    def delete_port_api(self, method=None, headers=None,
                            params=None, body=None, **kwargs):
        return info_delete_port(method=method, headers=headers,
                                    params=params, body=body, **kwargs)
 
    def create_stack_api(self, method=None, headers=None,
                            params=None, body=None, **kwargs):
        return info_create_stack(method=method, headers=headers,
                                    params=params, body=body, **kwargs)

    def get_stack_api(self, method=None, headers=None,
                         params=None, body=None, **kwargs):
        return info_get_stack(method=method, headers=headers,
                                params=params, body=body, **kwargs)

    def delete_stack_api(self, method=None, headers=None,
                         params=None, body=None, **kwargs):
        return info_delete_stack(method=method, headers=headers,
                                params=params, body=body, **kwargs)
    def get_stackres_api(self, method=None, headers=None,
                         params=None, body=None, **kwargs):
        return info_get_stackres(method=method, headers=headers,
                                 params=params, body=body, **kwargs)
