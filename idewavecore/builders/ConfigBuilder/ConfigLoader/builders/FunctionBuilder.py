from typing import Callable

from idewavecore.constants import (
    PACKAGE_ROOT,
    MIDDLEWARES_DIR,
    NATIVE_MIDDLEWARES_PREFIX,
)
from idewavecore.utils import import_function


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class FunctionBuilder:

    @staticmethod
    def build_from(function_path: str) -> Callable:
        function_path = f'{MIDDLEWARES_DIR}.{function_path}'

        if NATIVE_MIDDLEWARES_PREFIX in function_path:
            # remove prefix from path
            function_path = function_path.replace(
                f'{NATIVE_MIDDLEWARES_PREFIX}.', ''
            )
            function_path = f'{PACKAGE_ROOT}.{function_path}'

        return import_function(function_path)
