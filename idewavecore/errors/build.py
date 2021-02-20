class BuildError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MissedRequiredParamError(BuildError):
    def __init__(self, param_name: str):
        message = f'Required param "{param_name}" is missed'
        super().__init__(message)


class FunctionNotExistError(BuildError):
    def __init__(self, function_name: str):
        message = f'Function "{function_name}" does not exist'
        super().__init__(message)


class MissedItemError(BuildError):
    def __init__(self, item: str):
        message = f'Item "{item}" is missed. ' \
                  f'Check if function_path correct.'
        super().__init__(message)


class UnsupportedDBDialectError(BuildError):
    def __init__(self, dialect: str):
        message = f'Dialect "{dialect}" is not supported. ' \
                  f'See SUPPORTED_DIALECTS.'
        super().__init__(message)


class UnsupportedDBDriverError(BuildError):
    def __init__(self, driver_name: str):
        message = f'Driver "{driver_name}" is not supported. ' \
                  f'See SUPPORTED_DB_DRIVERS.'
        super().__init__(message)


class WrongDriverForDialectError(BuildError):
    def __init__(self, driver_name: str, dialect: str):
        message = f'Driver "{driver_name}" ' \
                  f'cannot be used with {dialect}. ' \
                  f'See SUPPORTED_DB_DRIVERS.'
        super().__init__(message)


class InvalidConfigError(BuildError):
    def __init__(self, config_path: str):
        message = f'Config path is invalid. ' \
                  f'"{config_path}" is incorrect value.'
        super().__init__(message)
