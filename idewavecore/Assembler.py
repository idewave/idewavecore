from typing import List

from idewavecore.builders import ConfigBuilder, ServerBuilder
from idewavecore.builders.DBConnectionBuilder import ConnectionMapBuilder
from idewavecore.network import BaseServer
from idewavecore.session.Storage import Storage


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class Assembler:
    def __init__(self, **kwargs):
        self.config_path: str = kwargs.pop('config_path')
        # TODO: create global storage here and just return it
        self.global_storage: Storage = kwargs.pop('global_storage')

    def assemble(self) -> List[BaseServer]:
        settings = ConfigBuilder.build_from(self.config_path).get('settings')

        connections_map = ConnectionMapBuilder\
            .build_from(settings.get('db_connections'))

        server_builder = ServerBuilder(
            global_storage=self.global_storage,
            connections_map=connections_map
        )

        return [
            server_builder.build_from(config)
            for config in settings.get('servers').values()
        ]
