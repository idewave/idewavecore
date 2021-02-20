from unittest import TestCase
from sqlalchemy.orm.session import Session

from idewavecore.builders import ConfigBuilder
from idewavecore.builders.DBConnectionBuilder import ConnectionMapBuilder
from idewavecore.errors.build import (
    WrongDriverForDialectError,
    UnsupportedDBDriverError,
    UnsupportedDBDialectError,
    MissedRequiredParamError,
)


TEST_MIDDLEWARES_CONFIG_PATH = 'test/mock_data/' \
                               'configs/db_connections.mock.yml'

TEST_DB_WITH_INCOMPATIBLE_CONFIG_PATH = 'test/mock_data/' \
                               'configs/db_with_incompatible.mock.yml'


class TestDBConnectionBuilder(TestCase):
    def test_connections_map_builded_successfully(self):
        config = ConfigBuilder \
            .build_from(TEST_MIDDLEWARES_CONFIG_PATH) \
            .get('db_connections')

        connections_map = ConnectionMapBuilder.build_from(config)

        self.assertTrue(
            {'sqlite',
             'mysql_pymysql',
             'postgresql_pygresql'} == connections_map.keys()
        )
        self.assertTrue(
            all(isinstance(connection, Session)
                for connection in connections_map.values())
        )

    def test_wrong_driver_when_dialect_has_no_supported_drivers_list(self):
        config = ConfigBuilder \
            .build_from(TEST_DB_WITH_INCOMPATIBLE_CONFIG_PATH) \
            .get('db_connections')

        with self.assertRaises(WrongDriverForDialectError) as context:
            ConnectionMapBuilder.build_from(
                {
                    'sqlite_with_mysql_driver':
                        config.get('sqlite_with_mysql_driver')
                }
            )

        self.assertTrue(isinstance(context.exception, WrongDriverForDialectError))
        self.assertTrue('Driver "pymysql" cannot be used with sqlite' in context.exception.args[0])

    def test_unsupported_driver_when_dialect_has_supported_drivers_list(self):
        config = ConfigBuilder \
            .build_from(TEST_DB_WITH_INCOMPATIBLE_CONFIG_PATH) \
            .get('db_connections')

        with self.assertRaises(UnsupportedDBDriverError) as context:
            ConnectionMapBuilder.build_from(
                {
                    'mysql_with_pygresql':
                        config.get('mysql_with_pygresql')
                }
            )

        self.assertTrue(isinstance(context.exception, UnsupportedDBDriverError))
        self.assertTrue('Driver "pygresql" is not supported' in context.exception.args[0])

    def test_unsupported_dialect(self):
        config = ConfigBuilder \
            .build_from(TEST_DB_WITH_INCOMPATIBLE_CONFIG_PATH) \
            .get('db_connections')

        with self.assertRaises(UnsupportedDBDialectError) as context:
            ConnectionMapBuilder.build_from(
                {
                    'unknown_dialect':
                        config.get('unknown_dialect')
                }
            )

        self.assertTrue(isinstance(context.exception, UnsupportedDBDialectError))
        self.assertTrue('Dialect "unknown" is not supported' in context.exception.args[0])

    def test_missed_dialect(self):
        config = ConfigBuilder \
            .build_from(TEST_DB_WITH_INCOMPATIBLE_CONFIG_PATH) \
            .get('db_connections')

        with self.assertRaises(MissedRequiredParamError) as context:
            ConnectionMapBuilder.build_from(
                {
                    'missed_dialect':
                        config.get('missed_dialect')
                }
            )

        self.assertTrue(isinstance(context.exception, MissedRequiredParamError))
        self.assertTrue('Required param "dialect" is missed' in context.exception.args[0])
