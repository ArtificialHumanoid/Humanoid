"""
See also "AI/Problem Design" and "AI/Protocols".
"""
from __future__ import annotations

from dataclasses import dataclass


class Literal:
    """Represent a literal by the name it is assigned in source."""

    __slots__ = ("name", "owner", "qualified_name")

    name: str | None
    owner: type[object] | None
    qualified_name: str | None

    def __init__(self) -> None:
        self.name = None
        self.owner = None
        self.qualified_name = None

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.name = name
        self.owner = owner
        self.qualified_name = f"{owner.__qualname__}.{name}"

    @property
    def value(self) -> str:
        """Return this literal's source name."""

        if self.name is None:
            raise ValueError("Literal has not been assigned to a class attribute.")
        return self.name

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        if self.qualified_name is None:
            return f"{type(self).__name__}()"
        return self.qualified_name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Literal):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return False

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass
class Actions:
    wait = Literal()
    type = Literal()

    @dataclass
    class Mouse:
        @dataclass
        class Click:
            left = Literal()
            right = Literal()
            middle = Literal()

        position = Literal()  # Combine with `wait` for hover.
        scroll = Literal()

    @dataclass
    class Run:
        os = Literal()
        python = Literal()
