from idewavecore.session import Storage
from idewavecore.crypto import Cypher


async def encrypt(**kwargs):
    session_storage: Storage = kwargs.pop('session_storage')
    cypher: Cypher = session_storage.get_value('cypher')
    request: bytes = session_storage.get_value('request')

    session_storage.set_items([
        {
            'request': {
                'value': cypher.encrypt(request)
            }
        }
    ])


async def decrypt(**kwargs):
    session_storage: Storage = kwargs.pop('session_storage')
    cypher: Cypher = session_storage.get_value('cypher')
    request: bytes = session_storage.get_value('request')

    session_storage.set_items([
        {
            'request': {
                'value': cypher.decrypt(request)
            }
        }
    ])

