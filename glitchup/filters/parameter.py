"""Defining configuration parameter of a filter"""


from __future__ import annotations

from enum import Enum, auto
from typing import Any, TypeAlias

__all__ = ("Parameter",)

RANGE: TypeAlias = tuple[int | float, int | float] | None


class Parameter:
    """Configurable parameter of a filter"""

    class Type(Enum):
        INT = auto()
        FLOAT = auto()

    def __init__(
        self, type_: Type, name: str, default: int | float, range_: RANGE = None
    ):
        self._type = type_
        self._name = name
        self._default = default
        self._range = range_

    @property
    def type(self) -> Type:
        """Type of the parameter"""
        return self._type

    @property
    def name(self) -> str:
        """Name of the parameter"""
        return self._name

    @property
    def default(self) -> int | float:
        """Default value of the parameter"""
        return self._default

    @property
    def range(self) -> RANGE:
        """Return the range of the parameter"""
        return self._range

    def __dict__(self) -> dict[str, Any]:
        return {
            "type": self._type.name,
            "name": self._name,
            "default": self._default,
            "range": self._range,
        }

    @staticmethod
    def from_dict(d: dict[str, Any]) -> Parameter:
        """Create a parameter from a dictionary"""
        return Parameter(Parameter.Type[d["type"]], d["name"], d["default"], d["range"])
