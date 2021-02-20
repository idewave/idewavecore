from typing import List, Callable
from functools import partial

from idewavecore.session import Storage

from .PipeBuilder import PipeBuilder


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class InfiniteLoopBuilder:

    @staticmethod
    def build_from(middlewares: List[Callable]) -> partial:
        pipe = PipeBuilder.build_from(middlewares)

        async def infinite_loop(*args, **kwargs) -> bool:
            _pipe: partial = args[0]

            while True:
                await _pipe(**kwargs)

                session_storage: Storage = kwargs.get('session_storage')
                should_break: bool = session_storage.get_value('should_break')

                if should_break:
                    break

            return True

        return partial(infinite_loop, pipe)
