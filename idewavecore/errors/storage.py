class StorageError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class OverwriteFrozenFieldError(StorageError):
    def __init__(self):
        message = 'Frozen field cannot be overwritten.'
        super().__init__(message)
