from unittest import TestCase
from functools import partial

from idewavecore.builders import ConfigBuilder
from idewavecore.builders.ConfigBuilder.\
    ConfigLoader.builders import RouterBuilder
from idewavecore.session import Storage, ItemFlag

from ..utils import async_test


TEST_MIDDLEWARES_CONFIG_PATH = 'test/mock_data/configs/middlewares.mock.yml'

ITERATIONS_LIMIT = 1000000


class TestRouterBuilder(TestCase):
    def setUp(self) -> None:
        self.middlewares = ConfigBuilder.build_from(
            TEST_MIDDLEWARES_CONFIG_PATH
        ).get('middlewares')

        self.session_storage = Storage()
        self.server_storage = Storage()
        self.global_storage = Storage()

    def test_infinite_loop_building(self):
        router: partial = RouterBuilder.build_from(
            self.middlewares.get('only_router')
        )
        self.assertEqual(router.func.__name__, 'router')

    @async_test
    async def test_inline_route_processing(self):
        router: partial = RouterBuilder.build_from(
            self.middlewares.get('only_router')
        )

        self.session_storage.set_items([
            {
                'route': {
                    'value': 'TEST_ROUTE_INLINE'
                }
            }
        ])

        await router(
            session_storage=self.session_storage,
            server_storage=self.server_storage,
            global_storage=self.global_storage
        )

        self.assertEqual(
            self.session_storage,
            {
                'mock_value': {
                    'value': 1,
                    'flags': ItemFlag.PERSISTENT
                }
            }
        )

    @async_test
    async def test_unexpected_route(self):
        router: partial = RouterBuilder.build_from(
            self.middlewares.get('only_router')
        )

        self.session_storage.set_items([
            {
                'route': {
                    'value': 'NOT_EXISTED_ROUTE'
                }
            }
        ])

        with self.assertRaises(ValueError) as context:
            await router(
                session_storage=self.session_storage,
                server_storage=self.server_storage,
                global_storage=self.global_storage
            )

        self.assertTrue(isinstance(context.exception, ValueError))
        self.assertTrue('Unexpected route' in context.exception.args[0])

    @async_test
    async def test_list_route_processing(self):
        router: partial = RouterBuilder.build_from(
            self.middlewares.get('only_router')
        )

        self.session_storage.set_items([
            {
                'route': {
                    'value': 'TEST_ROUTE_LIST'
                }
            }
        ])

        await router(
            session_storage=self.session_storage,
            server_storage=self.server_storage,
            global_storage=self.global_storage
        )

        self.assertEqual(
            self.session_storage,
            {
                'mock_value': {
                    'value': 3,
                    'flags': ItemFlag.PERSISTENT
                }
            }
        )
