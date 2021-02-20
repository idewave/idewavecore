from os import path
from yaml import load

from idewavecore.errors.build import InvalidConfigError
from .ConfigLoader import ConfigLoader


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class ConfigBuilder:

    @staticmethod
    def build_from(config_path: str):
        if path.isfile(config_path):
            with open(config_path) as stream:
                return load(stream, ConfigLoader)
        else:
            raise InvalidConfigError(config_path)
