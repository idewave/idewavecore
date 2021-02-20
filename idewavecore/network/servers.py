from asyncio import start_server, StreamReader, StreamWriter, coroutine
from websockets import serve, WebSocketCommonProtocol
from websockets.server import Serve
from typing import Generator, Optional, Callable

from idewavecore.debug.Logger import Logger
from idewavecore.session import Storage, ItemFlag

from .constants import CONNECTION_TYPE_TCP, CONNECTION_TYPE_WEBSOCKET
from .connections import ConnectionFactory, BaseConnection
from .proxies import BaseProxy


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class BaseServer:
    __slots__ = (
        'host', 'port', 'connection_type',
        'proxy', 'server_name', 'is_debug',
        'middlewares_entry', 'global_storage',
        'server_storage', '_instance'
    )

    def __init__(self, **kwargs):
        # connection
        self.host: str = kwargs.pop('host')
        self.port: int = kwargs.pop('port')
        self.connection_type: str = kwargs.pop('connection_type')
        # proxy
        self.proxy: Optional[BaseProxy] = kwargs.pop('proxy', None)
        # server options
        self.server_name: str = kwargs.pop('server_name')
        self.is_debug: bool = kwargs.pop('is_debug')
        # middlewares
        self.middlewares_entry: Callable = kwargs.pop('middlewares_entry')
        # storages
        self.global_storage: Storage = kwargs.pop('global_storage')
        self.server_storage: Storage = Storage(
            is_debug=self.is_debug,
            debug_name=f'Server Storage | {self.server_name}',
        )

        self._instance: Optional[Generator] = None

    def start(self):
        Logger.success(f'[{self.server_name}]: started...')

    def stop(self):
        Logger.info(f'[{self.server_name}]: stopping...')
        self._instance.close()

    async def handle_connection(self, *args):
        connection: BaseConnection = ConnectionFactory(
            self.connection_type
        ).get_connection(*args)

        self.server_storage.set_items([
            {
                connection.peer_name: {
                    'value': connection,
                    'flags': ItemFlag.PERSISTENT,
                }
            }
        ])

        session_storage = self._init_session_storage(
            sender=connection.peer_name
        )

        flags = ItemFlag.PERSISTENT
        session_storage.set_items([
            {
                'connection': {
                    'value': connection,
                    'flags': flags,
                }
            },
            {
                'proxy': {
                    'value': self.proxy,
                    'flags': flags
                }
            }
        ])

        completed = False
        # TODO: need to test if simple pipe can throw TimeoutError
        while not completed:
            try:
                completed = await self.middlewares_entry(
                    session_storage=session_storage,
                    server_storage=self.server_storage,
                    global_storage=self.global_storage,
                )
            except TimeoutError:
                continue

        Logger.info('Connection closed.')
        connection.close()

        self.server_storage.remove_items(keys=[connection.peer_name])

    def get(self):
        return self._instance

    def _init_session_storage(self, *args, **kwargs) -> Storage:
        sender = args[0] if args else kwargs.pop('sender')

        return Storage(
            is_debug=self.is_debug,
            debug_name=f'Session Storage | '
                       f'{self.server_name} | '
                       f'{sender}'
        )


class TCPServer(BaseServer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start(self):
        super().start()
        self._instance: coroutine = start_server(
            self.handle_connection,
            host=self.host,
            port=self.port
        )

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        await super().handle_connection(reader, writer)


class WebsocketServer(BaseServer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start(self):
        super().start()
        self._instance: Serve = serve(
            self.handle_connection,
            host=self.host,
            port=self.port
        )

    def stop(self):
        Logger.info(f'[{self.server_name}]: stopping...')
        self._instance.ws_server.close()

    async def handle_connection(self, websocket: WebSocketCommonProtocol, path: str):
        await super().handle_connection(websocket, path)


class ServerFactory:
    def __init__(self, connection_type: str):
        self.connection_type = connection_type

    def get_server(self, **kwargs) -> BaseServer:
        if self.connection_type == CONNECTION_TYPE_TCP:
            return TCPServer(**kwargs)
        elif self.connection_type == CONNECTION_TYPE_WEBSOCKET:
            return WebsocketServer(**kwargs)

        raise ValueError(f'Incorrect connection_type: "{self.connection_type}"')
