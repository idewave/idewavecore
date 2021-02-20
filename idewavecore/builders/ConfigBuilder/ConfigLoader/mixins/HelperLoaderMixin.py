from yaml import load
from os import path

from .BaseLoaderMixin import BaseLoaderMixin


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class HelperLoaderMixin(BaseLoaderMixin):

    # this line need to allow multiple inheritance
    # without this line only first Parent's yaml_constructors will be available
    yaml_constructors = BaseLoaderMixin.yaml_constructors

    def __init__(self, stream):
        super(HelperLoaderMixin, self).__init__(stream)
        if isinstance(stream, str):
            self._root = __file__
        else:
            self._root = path.split(stream.name)[0]

    def inject(self, node):
        filename = path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as file:
            return load(file, HelperLoaderMixin)


HelperLoaderMixin.add_constructor('!inject', HelperLoaderMixin.inject)
