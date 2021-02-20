from unittest import TestCase

from idewavecore.builders import ConfigBuilder, ProxyBuilder
from idewavecore.network import TCPProxy, WebsocketProxy


TEST_SERVER_CONFIG_PATH = 'test/mock_data/configs/proxies.mock.yml'


class TestProxyBuilder(TestCase):
    def setUp(self) -> None:
        self.settings = ConfigBuilder\
            .build_from(TEST_SERVER_CONFIG_PATH).get('proxies')

    def test_tcp_proxy_builder(self):
        config = self.settings.get('tcp_proxy')
        proxy = ProxyBuilder.build_from(config)

        self.assertTrue(isinstance(proxy, TCPProxy))

    def test_websocket_proxy_builder(self):
        config = self.settings.get('websocket_proxy')
        proxy = ProxyBuilder.build_from(config)

        self.assertTrue(isinstance(proxy, WebsocketProxy))
