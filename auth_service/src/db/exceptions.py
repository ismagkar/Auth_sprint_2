class EntityNotFound(Exception):
    pass


class UserNotFound(EntityNotFound):
    pass


class RoleNotFound(EntityNotFound):
    pass


class NotEnumEntity(Exception):
    pass


class RoleNotAuthenticated(NotEnumEntity):
    pass


class AlreadyExists(Exception):
    pass


class UserAlreadyExists(AlreadyExists):
    pass


class RoleAlreadyExists(AlreadyExists):
    pass
