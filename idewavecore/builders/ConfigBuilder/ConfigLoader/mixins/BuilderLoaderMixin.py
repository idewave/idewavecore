from typing import List, Callable, Dict, Union

from idewavecore.builders.ConfigBuilder.ConfigLoader.builders import (
    PipeBuilder,
    InfiniteLoopBuilder,
    RouterBuilder,
    FunctionBuilder
)

from .BaseLoaderMixin import BaseLoaderMixin


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class BuilderLoaderMixin(BaseLoaderMixin):

    # this line need to allow multiple inheritance
    # without this line only first Parent's yaml_constructors will be available
    yaml_constructors = BaseLoaderMixin.yaml_constructors

    def pipe(self, node):
        middlewares: List[Callable] = self.construct_sequence(node)
        return PipeBuilder.build_from(middlewares)

    def infinite_loop(self, node):
        middlewares: List[Callable] = self.construct_sequence(node)
        return InfiniteLoopBuilder.build_from(middlewares)

    def router(self, node):
        routes_handlers_map: Dict[str, Union[Callable, List[Callable]]] = \
            self.construct_mapping(node, deep=True)
        return RouterBuilder.build_from(routes_handlers_map)

    def fn(self, node):
        function_path = self.construct_scalar(node)
        return FunctionBuilder.build_from(function_path)


custom_tag_map = {
    '!pipe': BuilderLoaderMixin.pipe,
    '!infinite_loop': BuilderLoaderMixin.infinite_loop,
    '!router': BuilderLoaderMixin.router,
    '!fn': BuilderLoaderMixin.fn,
}

for name, func in custom_tag_map.items():
    BuilderLoaderMixin.add_constructor(name, func)
