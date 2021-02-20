from unittest import TestCase

from idewavecore.errors.storage import OverwriteFrozenFieldError
from idewavecore.session import Storage, ItemFlag

TEST_KEY = 'key'
TEST_VALUE = 'value'
TEST_ANOTHER_VALUE = 'another value'
TEST_NON_EXISTENT_KEY = 'this key not exists'


class TestStorage(TestCase):

    def setUp(self) -> None:
        self.storage = Storage()

    def test_set_and_get_item(self):
        self.storage.set_items([
            {
                TEST_KEY: {
                    'value': TEST_VALUE
                }
            }
        ])

        self.assertEqual(self.storage.get_value(TEST_KEY), TEST_VALUE)

    def test_clean_temporary_fields(self):
        self.storage.set_items([
            {
                TEST_KEY: {
                    'value': TEST_VALUE
                }
            }
        ])
        self.storage.clean_temporary_fields()

        self.assertIsNone(self.storage.get_value(TEST_KEY))

    def test_not_clean_persistent_fields(self):
        self.storage.set_items([
            {
                TEST_KEY: {
                    'value': TEST_VALUE,
                    'flags': ItemFlag.PERSISTENT
                }
            }
        ])
        self.storage.clean_temporary_fields()

        self.assertIsNotNone(self.storage.get_value(TEST_KEY))
        self.assertEqual(self.storage.get_value(TEST_KEY), TEST_VALUE)

    def test_cannot_change_frozen_field(self):
        self.storage.set_items([
            {
                TEST_KEY: {
                    'value': TEST_VALUE,
                    'flags': ItemFlag.FROZEN
                }
            }
        ])

        with self.assertRaises(OverwriteFrozenFieldError):
            self.storage._set_item(TEST_KEY, TEST_ANOTHER_VALUE)

        self.assertEqual(self.storage.get_value(TEST_KEY), TEST_VALUE)

    def test_get_non_existent_value(self):
        self.assertIsNone(self.storage.get_value(TEST_NON_EXISTENT_KEY))
