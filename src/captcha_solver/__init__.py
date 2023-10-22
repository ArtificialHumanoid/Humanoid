# pylint: disable=wildcard-import
from captcha_solver.solver import CaptchaSolver
from captcha_solver.error import *  # noqa
from pkg_resources import get_distribution

__version__ = get_distribution("Humanoid").version
