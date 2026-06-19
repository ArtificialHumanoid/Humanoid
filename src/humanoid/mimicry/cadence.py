from __future__ import annotations

import sys
from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
from inspect import isasyncgenfunction, iscoroutinefunction, isgeneratorfunction
from random import uniform
from time import sleep
from types import CodeType, FrameType
from typing import Any, Callable, Iterator, Optional, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])
_random_sleep_between_lines_enabled: ContextVar[bool] = ContextVar(
    "random_sleep_between_lines_enabled",
    default=True,
)


@contextmanager
def random_sleep_between_lines_disabled() -> Iterator[None]:
    """Temporarily disable line-sleep cadence for deterministic modeled tests."""

    token = _random_sleep_between_lines_enabled.set(False)
    try:
        yield
    finally:
        _random_sleep_between_lines_enabled.reset(token)


@contextmanager
def random_sleep_between_lines_enabled() -> Iterator[None]:
    """Temporarily force line-sleep cadence on for live-use test contexts."""

    token = _random_sleep_between_lines_enabled.set(True)
    try:
        yield
    finally:
        _random_sleep_between_lines_enabled.reset(token)


def random_sleep_between_lines(
    minimum_seconds: float = 0.05,
    maximum_seconds: float = 0.25,
) -> Callable[[F], F]:
    """
    Insert random sleeps between executed source lines.

    # Parameters
    ------------
    - `minimum_seconds`: shortest possible sleep duration.
    - `maximum_seconds`: longest possible sleep duration.

    # Returns
    ---------
    - `decorator`: decorator for a synchronous Python function.
    """
    if minimum_seconds < 0:
        raise ValueError("minimum_seconds must be non-negative")
    if maximum_seconds < 0:
        raise ValueError("maximum_seconds must be non-negative")
    if minimum_seconds > maximum_seconds:
        raise ValueError(
            "minimum_seconds must be less than or equal to maximum_seconds"
        )

    def decorator(function: F) -> F:
        if (
            isasyncgenfunction(function)
            or iscoroutinefunction(function)
            or isgeneratorfunction(function)
        ):
            raise TypeError(
                "random_sleep_between_lines requires a synchronous Python function"
            )

        function_code = getattr(function, "__code__", None)
        if not isinstance(function_code, CodeType):
            raise TypeError("random_sleep_between_lines requires a Python function")

        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            previous_trace = sys.gettrace()
            target_frame: Optional[FrameType] = None
            target_trace: Optional[Callable[..., Any]] = None
            first_line = True

            def call_trace(
                trace_function: Optional[Callable[..., Any]],
                frame: FrameType,
                event: str,
                arg: Any,
            ) -> Optional[Callable[..., Any]]:
                if trace_function is None:
                    return None
                result = trace_function(frame, event, arg)
                if result is None:
                    return None
                return cast(Callable[..., Any], result)

            def trace(
                frame: FrameType,
                event: str,
                arg: Any,
            ) -> Optional[Callable[..., Any]]:
                nonlocal first_line, target_frame, target_trace
                if frame is target_frame:
                    target_trace = call_trace(target_trace, frame, event, arg)
                    if event == "line":
                        if first_line:
                            first_line = False
                        elif _random_sleep_between_lines_enabled.get():
                            sleep(uniform(minimum_seconds, maximum_seconds))
                    return trace

                previous_local_trace = call_trace(previous_trace, frame, event, arg)
                if event == "call" and frame.f_code is function_code:
                    target_frame = frame
                    target_trace = previous_local_trace
                    first_line = True
                    return trace
                return previous_local_trace

            sys.settrace(trace)
            try:
                return function(*args, **kwargs)
            finally:
                sys.settrace(previous_trace)

        return cast(F, wrapper)

    return decorator
