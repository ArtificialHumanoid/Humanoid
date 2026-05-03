# pylint: disable=wildcard-import
import sys

if sys.version_info >= (3, 8):
    from importlib import metadata
else:  # pragma: no cover - Python < 3.8
    import importlib_metadata as metadata

from humanoid.captcha_solver.error import *  # noqa
from humanoid.captcha_solver.error import __all__ as _error_all
from humanoid.captcha_solver.solver import CaptchaSolver

__all__ = ("CaptchaSolver", *_error_all)
__version__ = metadata.version("Humanoid")
