from typing import Dict, Any

from .DBConnectionBuilder import DBConnectionBuilder


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class ConnectionMapBuilder:

    @staticmethod
    def build_from(config: Dict[str, Any]):
        return {
            connection_name: DBConnectionBuilder.build_from(settings)
            for connection_name, settings in config.items()
        }
