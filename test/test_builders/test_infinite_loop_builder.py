from unittest import TestCase
from functools import partial

from idewavecore.builders import ConfigBuilder
from idewavecore.builders.ConfigBuilder.\
    ConfigLoader.builders import InfiniteLoopBuilder
from idewavecore.session import Storage, ItemFlag

from ..utils import async_test


TEST_MIDDLEWARES_CONFIG_PATH = 'test/mock_data/configs/middlewares.mock.yml'

ITERATIONS_LIMIT = 1000


class TestInfiniteLoopBuilder(TestCase):
    def setUp(self) -> None:
        self.middlewares = ConfigBuilder.build_from(
            TEST_MIDDLEWARES_CONFIG_PATH
        ).get('middlewares')

        self.session_storage = Storage()
        self.server_storage = Storage()
        self.global_storage = Storage()

    def test_infinite_loop_building(self):
        infinite_loop: partial = InfiniteLoopBuilder.build_from(
            self.middlewares.get('only_infinite_loop')
        )
        self.assertEqual(infinite_loop.func.__name__, 'infinite_loop')

    @async_test
    async def test_infinite_loop_processing(self):
        infinite_loop: partial = InfiniteLoopBuilder.build_from(
            self.middlewares.get('only_infinite_loop')
        )

        middlewares_amount = len(
            self.middlewares.get('only_infinite_loop')[0].args[0].args[0]
        )

        iterations_amount = (
                ITERATIONS_LIMIT // middlewares_amount +
                (1 if ITERATIONS_LIMIT % middlewares_amount else 0)
        )
        self.session_storage.set_items([
            {
                'break_after': {
                    'value': ITERATIONS_LIMIT,
                    'flags': ItemFlag.PERSISTENT
                }
            }
        ])

        await infinite_loop(
            session_storage=self.session_storage,
            server_storage=self.server_storage,
            global_storage=self.global_storage
        )

        self.assertEqual(
            self.session_storage,
            {
                'break_after': {
                    'value': ITERATIONS_LIMIT,
                    'flags': ItemFlag.PERSISTENT
                },
                'mock_value': {
                    'value': middlewares_amount * iterations_amount,
                    'flags': ItemFlag.PERSISTENT
                },
                'should_break': {
                    'value': True,
                    'flags': ItemFlag.PERSISTENT
                }
            }
        )
