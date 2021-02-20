from json import dumps
from urllib.parse import ParseResult
from typing import NamedTuple, Dict, Any


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class HttpRequest(NamedTuple):

    method: str

    parsed_url: ParseResult

    headers: Dict[str, str]

    body: Dict[str, Any]

    def as_dict(self):
        fields = {
            'method': self.method,
            **self.parsed_url._asdict(),
            **self.headers,
        }

        if self.body:
            fields['body'] = self.body

        return fields

    def as_bytes(self):
        return dumps(self.as_dict()).encode()
