from unittest import TestCase
from unittest.mock import patch, Mock

from idewavecore.builders import ConfigBuilder, ServerBuilder
from idewavecore.network import TCPServer, WebsocketServer
from idewavecore.session import Storage


TEST_SERVER_CONFIG_PATH = 'test/mock_data/configs/server.mock.yml'


class TestServerBuilder(TestCase):
    def setUp(self) -> None:
        self.settings = ConfigBuilder\
            .build_from(TEST_SERVER_CONFIG_PATH).get('servers')

    @patch('idewavecore.session.Storage')
    def test_build_tcp_server(self, global_storage: Storage):
        server_builder = ServerBuilder(
            global_storage=global_storage,
            connections_map=Mock()
        )

        config = list(self.settings.values())[0]

        server = server_builder.build_from(config)
        self.assertTrue(isinstance(server, TCPServer))

    @patch('idewavecore.session.Storage')
    def test_build_websocket_server(self, global_storage: Storage):
        server_builder = ServerBuilder(
            global_storage=global_storage,
            connections_map=Mock()
        )

        config = list(self.settings.values())[1]

        server = server_builder.build_from(config)
        self.assertTrue(isinstance(server, WebsocketServer))
