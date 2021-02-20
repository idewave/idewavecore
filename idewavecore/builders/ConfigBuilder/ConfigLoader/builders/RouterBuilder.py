from typing import Dict, Callable, List, Union
from functools import partial

from idewavecore.session import Storage
from idewavecore.utils import to_list

from .PipeBuilder import PipeBuilder


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


ROUTE_HANDLERS = Union[Callable, List[Callable]]


class RouterBuilder:

    @staticmethod
    def build_from(routes_handlers_map: Dict[str, ROUTE_HANDLERS]) -> partial:
        routes_handlers_map = {
            key: PipeBuilder.build_from(to_list(functions))
            for key, functions in routes_handlers_map.items()
        }

        async def router(*args, **kwargs) -> bool:
            _routes_handlers_map: Dict[str, ROUTE_HANDLERS] = args[0]
            session_storage: Storage = kwargs.get('session_storage')
            route: str = session_storage.get_value('route')
            pipe = _routes_handlers_map.get(route)

            if not pipe:
                raise ValueError(f'Unexpected route: "{route}"')

            await pipe(**kwargs)

            return True

        return partial(router, routes_handlers_map)
