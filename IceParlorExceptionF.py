class IceParlorException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ConfigurationFileNotFoundError(IceParlorException):
    pass


class ValueNotALLOWEDError(IceParlorException):
    pass


class DuplicateParlorLocationError(IceParlorException):
    pass
