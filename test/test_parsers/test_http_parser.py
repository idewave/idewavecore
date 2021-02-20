from unittest import TestCase

from idewavecore.parsers import HttpParser, HttpRequest


MOCK_DATA = b'GET / HTTP/1.1' \
            b'\r\nHost: localhost:9999' \
            b'\r\nUser-Agent: test' \
            b'\r\nAccept: */*' \
            b'\r\nContent-Length: 24' \
            b'\r\nContent-Type: application/x-www-form-urlencoded' \
            b'\r\n' \
            b'\r\n{"some_data": "some_value"}'


class TestHttpParser(TestCase):
    def test_parse(self):
        http_request: HttpRequest = HttpParser.parse(MOCK_DATA)

        self.assertTrue(isinstance(http_request, HttpRequest))
        self.assertTrue(isinstance(http_request.as_dict(), dict))
        self.assertTrue(isinstance(http_request.as_bytes(), bytes))
