# pylint: disable=wildcard-import
from humanoid.captcha_solver.solver import CaptchaSolver
from humanoid.captcha_solver.error import *  # noqa

try:
    from importlib import metadata as importlib_metadata
except ImportError:  # pragma: no cover - Python < 3.8
    import importlib_metadata

__version__ = importlib_metadata.version("Humanoid")
