"""Transport-neutral browser action requests."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

from humanoid.actions.types import ActionRequest, ActionResult, PageSnapshot

BROWSER_NAVIGATE = "browser.navigate"
BROWSER_CLICK = "browser.click"
BROWSER_TYPE_TEXT = "browser.type_text"
BROWSER_EVALUATE = "browser.evaluate"
BROWSER_WAIT = "browser.wait"
BROWSER_SNAPSHOT = "browser.snapshot"


class BrowserActionAdapter(Protocol):
    """Adapter implemented by a concrete browser control transport."""

    def execute(
        self,
        action: ActionRequest,
        snapshot: PageSnapshot | None = None,
    ) -> ActionResult:
        """Execute one action request."""
        ...


def _defined_parameters(**parameters: Any) -> dict[str, Any]:
    return {key: value for key, value in parameters.items() if value is not None}


def action_request(
    name: str,
    parameters: Mapping[str, Any] | None = None,
    *,
    description: str | None = None,
) -> ActionRequest:
    """Build a generic action request."""

    normalized_name = str(name or "").strip()
    if not normalized_name:
        raise ValueError("name is required.")
    return ActionRequest(
        normalized_name,
        dict(parameters or {}),
        description=description,
    )


def navigate(url: str, *, description: str | None = None) -> ActionRequest:
    """Request navigation to a URL."""

    normalized_url = str(url or "").strip()
    if not normalized_url:
        raise ValueError("url is required.")
    return action_request(
        BROWSER_NAVIGATE,
        {"url": normalized_url},
        description=description,
    )


def click(
    *,
    selector: str | None = None,
    text: str | None = None,
    x: float | None = None,
    y: float | None = None,
    description: str | None = None,
) -> ActionRequest:
    """Request a click by selector, visible text, or viewport coordinates."""

    parameters = _defined_parameters(selector=selector, text=text, x=x, y=y)
    has_coordinates = "x" in parameters and "y" in parameters
    has_dom_target = bool(parameters.get("selector") or parameters.get("text"))
    if not has_coordinates and not has_dom_target:
        raise ValueError("click requires selector, text, or both x and y.")
    if ("x" in parameters) != ("y" in parameters):
        raise ValueError("click coordinates require both x and y.")
    return action_request(BROWSER_CLICK, parameters, description=description)


def type_text(
    text: str,
    *,
    selector: str | None = None,
    secret: bool = False,
    description: str | None = None,
) -> ActionRequest:
    """Request text entry without choosing a specific browser transport."""

    return action_request(
        BROWSER_TYPE_TEXT,
        _defined_parameters(selector=selector, text=str(text), secret=bool(secret)),
        description=description,
    )


def evaluate(script: str, *, description: str | None = None) -> ActionRequest:
    """Request JavaScript evaluation in the current page."""

    normalized_script = str(script or "").strip()
    if not normalized_script:
        raise ValueError("script is required.")
    return action_request(
        BROWSER_EVALUATE,
        {"script": normalized_script},
        description=description,
    )


def wait(seconds: float, *, description: str | None = None) -> ActionRequest:
    """Request a bounded wait before the next page classification."""

    if seconds < 0:
        raise ValueError("seconds must be non-negative.")
    return action_request(
        BROWSER_WAIT,
        {"seconds": float(seconds)},
        description=description,
    )


def snapshot(*, description: str | None = None) -> ActionRequest:
    """Request a fresh page snapshot."""

    return action_request(BROWSER_SNAPSHOT, description=description)
