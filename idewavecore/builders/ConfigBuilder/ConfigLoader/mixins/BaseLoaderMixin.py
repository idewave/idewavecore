from yaml import SafeLoader


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class BaseLoaderMixin(SafeLoader):

    # this line need to allow multiple inheritance
    yaml_constructors = SafeLoader.yaml_constructors.copy()
