from asyncio import open_connection, wait_for, sleep as async_sleep
from websockets import connect
from typing import Union

from .connections import (
    ConnectionFactory,
    CONNECTION
)
from .constants import (
    CONNECTION_TYPE_TCP,
    CONNECTION_TYPE_WEBSOCKET,
    MIN_TIMEOUT
)


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class BaseProxy:
    __slots__ = ('host', 'port', 'connection')

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connection: Union[CONNECTION, None] = None

    async def connect(self):
        ...

    async def read(self, *args, **kwargs):
        ...

    async def write(self, *args, **kwargs):
        ...


class TCPProxy(BaseProxy):
    async def connect(self) -> None:
        reader, writer = await open_connection(self.host, self.port)
        self.connection = ConnectionFactory(CONNECTION_TYPE_TCP)\
            .get_connection(reader, writer)

    async def read(self, amount: int) -> bytes:
        response = b''

        while True:
            data = await wait_for(
                self.connection.reader.read(amount),
                timeout=MIN_TIMEOUT
            )
            if not data:
                break

            response += data

            await async_sleep(MIN_TIMEOUT)

        return response

    async def write(self, request: bytes):
        self.connection.writer.write(request)
        await self.connection.writer.drain()


class WebsocketProxy(BaseProxy):
    async def connect(self) -> None:
        path: str = f'wss://{self.host}:{self.port}'
        websocket = await connect(path)
        self.connection = ConnectionFactory(CONNECTION_TYPE_WEBSOCKET)\
            .get_connection(websocket, path)

    async def read(self) -> bytes:
        response: bytes = await self.connection.websocket.recv()
        return response

    async def write(self, request: bytes):
        await self.connection.websocket.send(request)


class ProxyFactory:
    def __init__(self, connection_type: str):
        self.connection_type = connection_type

    def get_proxy(self, *args, **kwargs):
        if self.connection_type == CONNECTION_TYPE_TCP:
            return TCPProxy(*args, **kwargs)
        elif self.connection_type == CONNECTION_TYPE_WEBSOCKET:
            return WebsocketProxy(*args, **kwargs)

        raise ValueError(f'Incorrect connection_type: "{self.connection_type}"')
