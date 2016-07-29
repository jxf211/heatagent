# -*- coding:utf-8 -*-

import logging
import simplejson as json
from const import HTTP_OK
from const import HTTP_BAD_REQUEST
from const import HTTP_INTERNAL_SERVER_ERROR
from nova import get_all_hosts
from nova import get_host_detail_by_id

log = logging.getLogger(__name__)


def host_request(method=None, headers=None,
                 params=None, body=None, ip=None, **kwargs):
    try:
        log.info('entry.')
        hosts = get_all_hosts()
        for host in hosts['hypervisors']:
            host_detail = get_host_detail_by_id(host['id'])
            if host_detail['hypervisor']['host_ip'] == ip:
                break
        else:
            log.error('No Host (%s)' % ip)
            return HTTP_BAD_REQUEST, "{'ERROR': 'No Host (%s)'}" % ip
        return HTTP_OK, json.dumps(host_detail)
    except Exception as e:
        log.error(str(e))
        return HTTP_INTERNAL_SERVER_ERROR, "{'ERROR': %s}" % str(e)