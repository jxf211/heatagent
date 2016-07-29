# -*- coding:utf-8 -*-

import routes
import logging
import routes.middleware
import webob.dec
import webob.exc

log = logging.getLogger(__name__)

class Router(object):
    """WSGI middleware that maps incoming requests to WSGI apps."""

    def __init__(self, controller):
        """Create a router for the given routes.Mapper.
        """
        self.map = routes.Mapper()
        self.map.connect('/v1/info',
                         controller=controller,
                         action='info_api',
                         conditions=dict(method=['GET']))
        self.map.connect('/v1/images',
                         controller=controller,
                         action='get_images_api',
                         conditions=dict(method=['GET']))
        self.map.connect('/v1/flavors',
                         controller=controller,
                         action='get_flavors_api',
                         conditions=dict(method=['GET']))
        self.map.connect('/v1/vm',
                         controller=controller,
                         action='create_vm_api',
                         conditions=dict(method=['POST']))
        self.map.connect('/v1/vm/:vmuuid',
                         controller=controller,
                         action='delete_vm_api',
                         conditions=dict(method=['DELETE'])) 
        self.map.connect('/v1/networks',
                         controller=controller,
                         action='create_network_api',
                         conditions=dict(method=['POST']))
        self.map.connect('/v1/networks/:network_uuid',
                         controller=controller,
                         action='delete_network_api',
                         conditions=dict(method=['DELETE']))
        self.map.connect('/v1/subnets/',
                         controller=controller,
                         action='create_subnet_api',
                         conditions=dict(method=['POST']))
        self.map.connect('/v1/subnets/:subnet_uuid',
                         controller=controller,
                         action='delete_subnet_api',
                         conditions=dict(method=['DELETE']))
        self.map.connect('/v1/ports/',
                         controller=controller,
                         action='create_port_api',
                         conditions=dict(method=['POST']))
        self.map.connect('/v1/ports/:port_uuid',
                         controller=controller,
                         action='delete_port_api',
                         conditions=dict(method=['DELETE']))
        self.map.connect('/v1/nsp/host/:ip',
                         controller=controller,
                         action='host_api',
                         conditions=dict(method=['GET']))
        self.map.connect('/v1/stack/',
                         controller=controller,
                         action='create_stack_api',
                         conditions=dict(method=['POST']))
        self.map.connect('/v1/stack/:stack_name',
                         controller=controller,
                         action='get_stack_api',
                         conditions=dict(method=['GET']))
        self.map.connect('/v1/stack/:stack_name',
                         controller=controller,
                         action='delete_stack_api',
                         conditions=dict(method=['DELETE']))
        self.map.connect('/v1/stack/:stack_name/resources',
                        controller=controller,
                        action='get_stackres_api',
                        onditions=dict(method=['GET']))
        self._router = routes.middleware.RoutesMiddleware(self._dispatch,
                                                          self.map)

    @webob.dec.wsgify()
    def __call__(self, req):
        """Route the incoming request to a controller based on self.map.
        """
        return self._router

    @staticmethod
    @webob.dec.wsgify()
    def _dispatch(req):
        """Dispatch the request to the appropriate controller.
        """
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            log.debug('router not found:404')
            return webob.exc.HTTPNotFound()

        app = match['controller']
        return app
