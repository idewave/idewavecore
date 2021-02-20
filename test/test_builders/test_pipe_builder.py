from unittest import TestCase
from functools import partial

from idewavecore.builders import ConfigBuilder
from idewavecore.builders.ConfigBuilder.\
    ConfigLoader.builders import PipeBuilder
from idewavecore.session import Storage, ItemFlag

from ..utils import async_test


TEST_MIDDLEWARES_CONFIG_PATH = 'test/mock_data/configs/middlewares.mock.yml'


class TestPipeBuilder(TestCase):
    def setUp(self) -> None:
        self.middlewares = ConfigBuilder.build_from(
            TEST_MIDDLEWARES_CONFIG_PATH
        ).get('middlewares')

        self.session_storage = Storage()
        self.server_storage = Storage()
        self.global_storage = Storage()

    def test_pipe_building(self):
        pipe: partial = PipeBuilder.build_from(
            self.middlewares.get('only_fn')
        )
        self.assertEqual(pipe.func.__name__, 'pipe')

    @async_test
    async def test_pipe_processing(self):
        pipe: partial = PipeBuilder.build_from(
            self.middlewares.get('only_fn')
        )

        await pipe(
            session_storage=self.session_storage,
            server_storage=self.server_storage,
            global_storage=self.global_storage
        )

        self.assertEqual(
            self.session_storage,
            {
                'mock_value': {
                    'value': 2,
                    'flags': ItemFlag.PERSISTENT
                }
            }
        )
        self.assertEqual(self.session_storage.get_value('mock_value'), 2)
