from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from typing import Dict, Any

from .constants import SUPPORTED_DIALECTS, SUPPORTED_DB_DRIVERS
from idewavecore.errors.build import (
    MissedRequiredParamError,
    UnsupportedDBDialectError,
    UnsupportedDBDriverError,
    WrongDriverForDialectError,
)


__author__ = 'Sergio Ivanuzzo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2021, Idewavecore'


class DBConnectionBuilder:

    @staticmethod
    def build_from(config: Dict[str, Any]) -> Session:
        connection_string = DBConnectionBuilder.build_connection_string(config)
        engine = create_engine(connection_string)
        session_factory = sessionmaker(expire_on_commit=False, bind=engine)

        return scoped_session(session_factory)()

    @staticmethod
    def build_connection_string(config: Dict[str, Any]):
        dialect: str = config.get('dialect')
        driver: str = config.get('driver')
        user: str = config.get('user')
        password: str = config.get('password')
        host: str = config.get('host')
        port: int = config.get('port')
        db_name: str = config.get('db_name')
        charset: str = config.get('charset')

        if not dialect:
            raise MissedRequiredParamError('dialect')

        if dialect not in SUPPORTED_DIALECTS:
            raise UnsupportedDBDialectError(dialect)

        if driver:
            supported_drivers = SUPPORTED_DB_DRIVERS.get(dialect)
            if not supported_drivers:
                raise WrongDriverForDialectError(
                    driver_name=driver,
                    dialect=dialect,
                )

            if driver not in supported_drivers:
                raise UnsupportedDBDriverError(driver_name=driver)

            driver = f'+{driver}'

        connection_string = f'{dialect}{driver or ""}://'
        if user:
            connection_string += f'{user}'
            # connection string can contain empty password
            if password:
                connection_string += f':{password}'

        # some dbs (sqlite) not need host
        if host:
            connection_string += f'@{host}'
            if port:
                connection_string += f':{port}'

        if db_name:
            connection_string += f'/{db_name}'

        if charset:
            connection_string += f'?charset={charset}'

        return connection_string
