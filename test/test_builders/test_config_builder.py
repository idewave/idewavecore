from unittest import TestCase

from idewavecore.builders import ConfigBuilder
from idewavecore.errors.build import InvalidConfigError


TEST_CONFIG_PATH = 'test/mock_data/configs/settings.mock.yml'


class TestConfigBuilder(TestCase):

    def test_config_building(self):
        config = ConfigBuilder.build_from(
            TEST_CONFIG_PATH
        )

        self.assertIsInstance(config, dict)
        self.assertTrue('settings' in config)
        self.assertTrue('servers' in config['settings'])
        self.assertTrue('db_connections' in config['settings'])

    def test_invalid_path_processing(self):
        with self.assertRaises(InvalidConfigError) as context:
            ConfigBuilder.build_from('INVALID_PATH')

        self.assertTrue(isinstance(context.exception, InvalidConfigError))
        self.assertTrue('Config path is invalid' in context.exception.args[0])
