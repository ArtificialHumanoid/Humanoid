"""Safety helpers for action metadata."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from humanoid.actions.types import ActionResult

SECRET_VALUES_RETURNED_KEY = "secret_values_returned"
SENSITIVE_KEYWORDS: tuple[str, ...] = (
    "api_key",
    "authorization",
    "credential",
    "otp",
    "passcode",
    "password",
    "secret",
    "token",
)


def mark_no_secret_values(metadata: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Return metadata with an explicit no-secret-values marker."""

    result = dict(metadata or {})
    result[SECRET_VALUES_RETURNED_KEY] = False
    return result


def status_result(
    status: str,
    *,
    action: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ActionResult:
    """Build a status-only action result that declares no secrets were returned."""

    return ActionResult(
        str(status),
        action=action,
        metadata=mark_no_secret_values(metadata),
        secret_values_returned=False,
    )


def redact_sensitive_mapping(
    mapping: Mapping[str, Any],
    *,
    redaction: str = "[redacted]",
    sensitive_keywords: tuple[str, ...] = SENSITIVE_KEYWORDS,
) -> dict[str, Any]:
    """Redact values whose keys are likely to carry credentials or secrets."""

    redacted: dict[str, Any] = {}
    for key, value in mapping.items():
        normalized_key = str(key).casefold()
        if any(keyword in normalized_key for keyword in sensitive_keywords):
            redacted[key] = redaction
        else:
            redacted[key] = value
    return redacted
