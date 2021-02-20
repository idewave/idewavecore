from typing import Optional, List

from idewavecore.session import Storage
from idewavecore.network import BaseConnection


async def read(**kwargs):
    session_storage: Storage = kwargs.pop('session_storage')
    connection: BaseConnection = session_storage.get_value('connection')
    request: bytes = await connection.read()

    session_storage.set_items([
        {
            'request': {
                'value': request
            }
        }
    ])


async def read_into_buffer(**kwargs):
    await read(**kwargs)
    session_storage: Storage = kwargs.pop('session_storage')
    request: bytes = session_storage.get_value('request')
    buffer: Optional[bytes] = session_storage.get_value('buffer') or b''

    session_storage.set_items([
        {
            'buffer': {
                'value': buffer + request
            }
        }
    ])


async def write(**kwargs):
    session_storage: Storage = kwargs.pop('session_storage')
    connection: BaseConnection = session_storage.get_value('connection')
    response: bytes = session_storage.get_value('response')

    await connection.write(response)


async def write_from_buffer(**kwargs):
    session_storage: Storage = kwargs.pop('session_storage')
    buffer: Optional[bytes] = session_storage.get_value('buffer') or b''
    connection: BaseConnection = session_storage.get_value('connection')
    write_length: BaseConnection = session_storage.get_value('write_length')

    response: bytes = buffer[0:write_length]

    await connection.write(response)


async def broadcast(**kwargs):
    session_storage: Storage = kwargs.pop('session_storage')
    server_storage: Storage = kwargs.pop('server_storage')
    connections: List[BaseConnection] = (
            session_storage.get_value('connections')
            or server_storage.get_value('connections')
    )
    response: bytes = session_storage.get_value('response')

    for connection in connections:
        await connection.write(response)


async def proxy(**kwargs):
    session_storage: Storage = kwargs.pop('session_storage')
    proxy_connection = session_storage.get_value('proxy_connection')
    request: bytes = session_storage.get_value('request')

    response = await proxy_connection.send(request)
    session_storage.set_items([
        {
            'response': {
                'value': response
            }
        }
    ])
