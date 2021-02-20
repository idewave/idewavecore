from re import sub
from json import loads
from urllib.parse import urlparse, ParseResult
from typing import Tuple, Dict, Any, Optional, List

from idewavecore.debug import Logger

from .HttpRequest import HttpRequest
from .constants import HTTP_METHODS


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class HttpParser:

    @staticmethod
    def parse(data: bytes):
        if not data:
            Logger.warning('No data passed to HttpParser')
            return None
        else:
            items = data.decode('utf-8').split('\r\n')
            method, parsed_url = HttpParser.parse_start_line(items[0])

            headers, last_line = items[1:-2], items[-1]

            body: Optional[Dict[str, Any]] = None

            if last_line != '':
                body = loads(last_line)

            return HttpRequest(
                method=method,
                parsed_url=parsed_url,
                headers=HttpParser.parse_headers(headers),
                body=body
            )

    @staticmethod
    def parse_header(item: str):
        key, value = item.split(':', 1)
        return {key: value.strip()}

    @staticmethod
    def parse_headers(items: List[str]) -> Dict[str, str]:
        headers: List[Dict[str, str]] = [
            HttpParser.parse_header(header)
            for header in items
            if header != ''
        ]

        return {
            name: value
            for header in headers
            for name, value in header.items()
        }

    @staticmethod
    def parse_start_line(start_line: str) -> Tuple[str, ParseResult]:
        item = start_line

        method: str = next(
            method
            for method in HTTP_METHODS
            if method in item
        )

        item = sub(method, '', item)
        item = sub(r'HTTP/\d\.\d', '', item).strip()
        parsed_url = urlparse(item)

        return method, parsed_url
