"""Click adapters for browsing agents."""

from __future__ import annotations

from typing import Any, Protocol

from humanoid.actions import browser
from humanoid.actions.types import ActionRequest


__all__ = [
    "advance_debug_page_click",
    "click",
]


class DebugPageClickModule(Protocol):
    """Protocol for the shared screen click helper."""

    def advance_debug_page_click(
        self,
        debug_url: str,
        expected_state_description: str,
        **kwargs: Any,
    ) -> Any:
        """Advance a debug page by resolving and performing a click."""
        ...


def click(
    *,
    selector: str | None = None,
    text: str | None = None,
    x: float | None = None,
    y: float | None = None,
    description: str | None = None,
) -> ActionRequest:
    """Build a transport-neutral browser click request."""

    return browser.click(
        selector=selector,
        text=text,
        x=x,
        y=y,
        description=description,
    )


def advance_debug_page_click(
    debug_url: str,
    expected_state_description: str,
    *,
    screen_click: DebugPageClickModule,
    **kwargs: Any,
) -> Any:
    """
    Delegate debug-page click advancement to an injected screen helper.

    Humanoid owns the browsing action vocabulary.  Host applications provide
    concrete click resolution through `screen_click`.
    """

    return screen_click.advance_debug_page_click(
        debug_url,
        expected_state_description,
        **kwargs,
    )
