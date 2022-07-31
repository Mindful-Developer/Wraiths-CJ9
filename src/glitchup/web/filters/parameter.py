from __future__ import annotations

from enum import Enum, auto
from typing import Any, TypeAlias

from attrs import define, field

__all__ = ("Parameter", "ParamType")

PARAM_VALUE: TypeAlias = int | float | str
PARAM_RANGE: TypeAlias = tuple[PARAM_VALUE, ...]


class ParamType(Enum):
    """Enum for the types of parameters."""

    INT = auto()
    FLOAT = auto()
    ENUM = auto()


@define
class Parameter:
    """Configurable parameter of a filter"""

    _param_type: ParamType
    _name: str
    _default: PARAM_VALUE
    _param_range: PARAM_RANGE | None = field(default=None)

    @property
    def param_type(self) -> ParamType:
        """Type of the parameter"""
        return self._param_type

    @property
    def name(self) -> str:
        """Name of the parameter"""
        return self._name

    @property
    def default(self) -> PARAM_VALUE:
        """Default value of the parameter"""
        return self._default

    @property
    def param_range(self) -> PARAM_RANGE | None:
        """Return the range of the parameter"""
        return self._param_range

    def to_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the parameter"""
        return {
            "type": self.param_type.name,
            "name": self.name,
            "default": self.default,
            "range": self.param_range,
        }

    @staticmethod
    def from_dict(d: dict[str, Any]) -> Parameter:
        """Create a parameter from a dictionary"""
        return Parameter(
            d["type"],
            d["name"],
            d["default"],
            d["range"],
        )
