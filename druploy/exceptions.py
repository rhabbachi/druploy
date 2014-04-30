# vim: set syntax=python ts=4 sw=4 expandtab:

class AgileProjectError(Exception):
    pass


class CreateError(AgileProjectError):
    pass


class AlreadyExistsError(CreateError):
    pass


class ValidationError(AgileProjectError):
    pass


