from unittest import TestCase
from unittest.mock import patch

from idewavecore import Assembler
from idewavecore.network import BaseServer
from idewavecore.session import Storage


TEST_SERVER_CONFIG_PATH = 'test/mock_data/configs/settings.mock.yml'


class TestAssembler(TestCase):

    @patch('idewavecore.session.Storage')
    def test_assemble_from_config(self, global_storage: Storage):
        assembler = Assembler(
            global_storage=global_storage,
            config_path=TEST_SERVER_CONFIG_PATH
        )

        self.assertTrue(isinstance(assembler, Assembler))

        servers = assembler.assemble()

        for server in servers:
            self.assertTrue(isinstance(server, BaseServer))
