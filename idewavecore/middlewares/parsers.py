from idewavecore.parsers import HttpParser
from idewavecore.session import Storage


async def parse_http(**kwargs):
    session_storage: Storage = kwargs.pop('session_storage')
    request: bytes = session_storage.get_value('request')

    http_request = HttpParser.parse(request)

    session_storage.set_items([
        {
            'json_request': {
                'value': http_request.as_dict()
            }
        },
        {
            'response': {
                'value': http_request.as_bytes()
            }
        }
    ])
