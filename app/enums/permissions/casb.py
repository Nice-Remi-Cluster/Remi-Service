from enum import StrEnum


class RoleEnum(StrEnum):
    """
    Enum for CASB roles.
    """
    ADMIN = "admin"
    REGISTERED_USER = "registered_user"
    GUEST = "guest"

PREDIFINED_PERMISSIONS = [
    # (role, domain, resource, action, effect)
    ("guest")
]

