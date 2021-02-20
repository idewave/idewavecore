from typing import Any, Dict, List, Optional

from idewavecore.debug import Logger
from idewavecore.errors.storage import OverwriteFrozenFieldError
from idewavecore.utils import get_slots_items

from .constants import ItemFlag


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class Item:
    __slots__ = (
        'value',
        'flags',
    )

    def __init__(self, value: Any, flags: ItemFlag):
        self.value: Any = value
        self.flags: ItemFlag = flags or ItemFlag.NONE

    def __repr__(self):
        return f'{get_slots_items(self)}'

    def __eq__(self, other: Any):
        if isinstance(other, dict):
            items = get_slots_items(self)
            return items == other

        return False


class Storage:
    __slots__ = (
        '_items',
        'is_debug',
        'debug_name'
    )

    def __init__(self, **kwargs):
        self._items = {}
        self.is_debug: bool = kwargs.pop('is_debug', False)
        self.debug_name: str = kwargs.pop('debug_name', None)

    def get_value(self, key: str):
        item: Item = self._items.get(key)
        return item.value if item else None

    def has_item(self, key: str):
        return key in self._items

    def set_items(self, items: List[Dict[str, Any]]):
        for item in items:
            key, value = list(item.items())[0]
            self._set_item(key, **value)

    def remove_items(self, keys: List[str]):
        for key in keys:
            self._items.pop(key, None)

    def remove_item(self, key):
        self._items.pop(key, None)

    def clean_temporary_fields(self):
        keys_to_remove = [
            key
            for key, item in self._items.items()
            if not item.flags & ItemFlag.PERSISTENT
        ]
        self.remove_items(keys_to_remove)

    def _set_item(
            self,
            key: str,
            value: Any,
            flags: Optional[ItemFlag] = None
    ):
        # check flags for existing item
        if self.has_item(key):
            flags: ItemFlag = self._items[key].flags

            if flags & ItemFlag.FROZEN:
                raise OverwriteFrozenFieldError()

        self._items[key] = Item(
            value=value,
            flags=flags
        )

        if self.is_debug:
            Logger.debug(
                f'[{self.debug_name}]:',
                f'[FUNCTION "set_item"]'
                f'[KEY={key}; VALUE={value}; FLAGS={flags}]\n'
            )

    def __repr__(self):
        return f'{self._items}'

    def __eq__(self, other: Any):
        if isinstance(other, dict):
            return self._items == other

        return False
