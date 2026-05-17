from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    CONTRIBUTOR = "contributor"
    USER = "user"


ROLE_HIERARCHY = {
    UserRole.USER: 0,
    UserRole.CONTRIBUTOR: 10,
    UserRole.ADMIN: 100,
}


def normalize_role(role: str | None) -> UserRole:
    try:
        return UserRole(role or UserRole.USER)
    except ValueError:
        return UserRole.USER


def has_minimum_role(actual: str | None, required: UserRole) -> bool:
    actual_role = normalize_role(actual)
    return ROLE_HIERARCHY[actual_role] >= ROLE_HIERARCHY[required]
