from importlib import import_module
from types import ModuleType
from typing import Dict, Any

from idewavecore.errors.build import FunctionNotExistError


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


def import_function(function_path: str):
    module_path, function_name = function_path.rsplit('.', 1)

    module: ModuleType = import_module(module_path)
    if not module.__dict__.get(function_name):
        raise FunctionNotExistError(function_name)

    return getattr(module, function_name)


def to_list(data: Any):
    return data if isinstance(data, list) else [data]


def get_slots_items(target: object) -> Dict[str, Any]:
    if isinstance(target, object):
        if getattr(target, '__slots__'):
            return {
                key: getattr(target, key)
                for key in target.__slots__
            }
        else:
            raise AttributeError('Target object have no __slots__')

    raise TypeError('Only object should be passed to this function')
