"""Shared action types for browser-oriented agents."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class PageSnapshot:
    """A compact, transport-neutral view of a browser page."""

    url: str | None = None
    title: str | None = None
    text: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def as_mapping(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "text": self.text,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ActionRequest:
    """A semantic action request independent of its execution transport."""

    name: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    description: str | None = None

    def as_mapping(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": self.name,
            "parameters": dict(self.parameters),
        }
        if self.description:
            payload["description"] = self.description
        return payload


@dataclass(frozen=True)
class ActionResult:
    """Status metadata returned after executing one semantic action."""

    status: str
    action: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    page: PageSnapshot | None = None
    secret_values_returned: bool = False

    def as_mapping(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "status": self.status,
            "secret_values_returned": self.secret_values_returned,
            "metadata": dict(self.metadata),
        }
        if self.action:
            payload["action"] = self.action
        if self.page:
            payload["page"] = self.page.as_mapping()
        return payload


class PageClassifier(Protocol):
    """Classify the current page state before choosing an action."""

    def __call__(self, snapshot: PageSnapshot) -> str:
        """Return a stable state label."""
        ...


class ActionChooser(Protocol):
    """Choose the next action for a classified page state."""

    def __call__(
        self,
        state: str,
        snapshot: PageSnapshot,
    ) -> ActionRequest | None:
        """Return the next action, or None when no action should run."""
        ...


class ActionExecutor(Protocol):
    """Execute one semantic action through a concrete browser transport."""

    def __call__(
        self,
        action: ActionRequest,
        snapshot: PageSnapshot,
    ) -> ActionResult:
        """Return action status and the next page snapshot when available."""
        ...
