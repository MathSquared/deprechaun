from typing import Any


_SYSTEMS: dict[str, Any] = {}  # TODO define functions that must be registered for a system


class SystemData:
    """The data needed by a depreciation system.

    Each depreciation system should define its own subclass that contains all data it needs.
    """
    pass


def systems() -> list[str]:
    return list(_SYSTEMS.keys())


def system(name: str) -> Any:
    return _SYSTEMS[name]


# TODO define function for registering a system
