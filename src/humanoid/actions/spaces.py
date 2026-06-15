"""
See also "AI/Problem Design" and "AI/Protocols".
"""
from dataclasses import dataclass

from utilities.meta.types_management import Literal


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
