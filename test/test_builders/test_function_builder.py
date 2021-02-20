from unittest import TestCase
from typing import Callable

from idewavecore.builders.ConfigBuilder.\
    ConfigLoader.builders import FunctionBuilder
from idewavecore.session import Storage, ItemFlag

from ..utils import async_test


TEST_MIDDLEWARE_PATH = 'native.test.mock_middleware'


class TestFunctionBuilder(TestCase):

    def test_function_building(self):
        function: Callable = FunctionBuilder.build_from(TEST_MIDDLEWARE_PATH)
        self.assertEqual(function.__name__, 'mock_middleware')

    @async_test
    async def test_function_processing(self):
        function: Callable = FunctionBuilder.build_from(TEST_MIDDLEWARE_PATH)
        session_storage = Storage()

        await function(session_storage=session_storage)

        self.assertEqual(
            session_storage,
            {
                'mock_value': {
                    'value': 1,
                    'flags': ItemFlag.PERSISTENT
                }
            }
        )
