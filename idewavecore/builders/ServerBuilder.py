from typing import Dict, Any

from idewavecore.debug import Logger
from idewavecore.network import (
    BaseServer,
    ServerFactory,
)
from idewavecore.session import Storage

from .ProxyBuilder import ProxyBuilder


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class ServerBuilder:

    __slots__ = (
        'global_storage',
        'connections_map'
    )

    def __init__(self, **kwargs):
        self.global_storage: Storage = kwargs.pop('global_storage')
        self.connections_map: Dict[str, Any] = kwargs.pop('connections_map')

    def build_from(self, config: Dict[str, Any]) -> BaseServer:
        connection = config.get('connection')
        options = config.get('options')

        proxy_settings = config.get('proxy')

        Logger.info(f'Building server "{options.get("server_name")}"')

        middlewares_entry = config.get('middlewares')
        db_connection_name = config.get('db_connection')

        params = {
            **connection,
            **options,
            'middlewares_entry': middlewares_entry,
            'global_storage': self.global_storage,
            'db_connection': self.connections_map.get(db_connection_name),
        }

        if proxy_settings:
            params['proxy'] = ProxyBuilder.build_from(proxy_settings)

        connection_type = connection.get('connection_type')
        if not connection_type:
            Logger.error('Connection type is required')

        return ServerFactory(connection_type).get_server(**params)
