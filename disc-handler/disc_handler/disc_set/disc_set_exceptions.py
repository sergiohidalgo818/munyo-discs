class DiscSetException(Exception):
    pass


class DiscSetFileNotFound(DiscSetException):
    pass


class DiscSetRepeatedDisc(DiscSetException):
    pass


class DiscSetNotSuchDisc(DiscSetException):
    pass
