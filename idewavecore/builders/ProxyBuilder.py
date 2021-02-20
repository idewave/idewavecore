from typing import Dict, Any

from idewavecore.network import ProxyFactory


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class ProxyBuilder:

    @staticmethod
    def build_from(config: Dict[str, Any]):
        connection_type = config.get('connection_type')
        host = config.get('host')
        port = config.get('port')

        return ProxyFactory(connection_type).get_proxy(host, port)
