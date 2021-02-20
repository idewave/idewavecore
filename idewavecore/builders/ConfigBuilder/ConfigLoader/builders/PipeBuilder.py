from typing import List, Callable
from functools import partial

from idewavecore.session import Storage


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class PipeBuilder:

    @staticmethod
    def build_from(middlewares: List[Callable]) -> partial:

        if not middlewares:
            raise ValueError('Middlewares list cannot be empty.')

        if not isinstance(middlewares, list):
            raise TypeError(
                'Only list can be passed to builder.'
            )

        if not all(isinstance(func, Callable) for func in middlewares):
            raise ValueError(
                'Each item in middlewares list should be function.'
            )

        async def pipe(functions: List[Callable], **kwargs) -> bool:
            session_storage: Storage = kwargs.get('session_storage')
            server_storage: Storage = kwargs.get('server_storage')
            global_storage: Storage = kwargs.get('global_storage')

            for function in functions:
                print(function)
                await function(**kwargs)

            session_storage.clean_temporary_fields()
            server_storage.clean_temporary_fields()
            global_storage.clean_temporary_fields()

            return True

        return partial(pipe, middlewares)
