from enum import IntFlag, auto


class ItemFlag(IntFlag):
    NONE = auto()
    # field will not be cleaned by Storage:clean_temporary_fields
    PERSISTENT = auto()
    # make this field constant
    FROZEN = auto()
