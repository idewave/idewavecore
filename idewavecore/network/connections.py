from asyncio import StreamReader, StreamWriter, wait_for
from websockets import WebSocketCommonProtocol
from typing import Union

from .constants import (
    MAX_READ_BYTES,
    MIN_TIMEOUT,
    CONNECTION_TYPE_TCP,
    CONNECTION_TYPE_WEBSOCKET,
)


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class BaseConnection:

    __slots__ = ('peer_name',)

    async def read(self):
        ...

    async def write(self, response: bytes):
        ...

    def close(self):
        ...

    def __repr__(self):
        items = {
            key: getattr(self, key) for key in self.__slots__
        }

        return f'{items}'


class TCPConnection(BaseConnection):
    __slots__ = ('reader', 'writer', 'peer_name')

    def __init__(self, *args, **kwargs):
        self.reader: StreamReader = args[0] if args else kwargs.pop('reader')
        self.writer: StreamWriter = args[1] if args else kwargs.pop('writer')

        peer_name = self.writer.get_extra_info('peername')
        self.peer_name = f'{peer_name[0]}:{peer_name[1]}'

    async def read(self) -> bytes:
        return await wait_for(
            self.reader.read(MAX_READ_BYTES),
            timeout=MIN_TIMEOUT
        )

    async def write(self, response: bytes) -> None:
        self.writer.write(response)
        await self.writer.drain()

    def close(self):
        self.writer.close()


class WebsocketConnection(BaseConnection):
    __slots__ = ('websocket', 'path', 'peer_name')

    def __init__(self, *args, **kwargs):
        self.websocket: WebSocketCommonProtocol = args[0] or kwargs.pop('websocket')
        self.path: str = args[1] or kwargs.pop('path')
        self.peer_name = self.websocket.remote_address

    async def read(self) -> bytes:
        return await self.websocket.recv()

    async def write(self, response: bytes) -> None:
        await self.websocket.send(response)


CONNECTION = Union[TCPConnection, WebsocketConnection]


class ConnectionFactory:
    def __init__(self, connection_type: str):
        self.connection_type = connection_type

    def get_connection(self, *args, **kwargs) -> CONNECTION:
        if self.connection_type == CONNECTION_TYPE_TCP:
            connection = TCPConnection
        elif self.connection_type == CONNECTION_TYPE_WEBSOCKET:
            connection = WebsocketConnection
        else:
            raise ValueError('Unknown connection type')

        return connection(*args, **kwargs)
