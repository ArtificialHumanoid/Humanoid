"""CAPTCHA and human-verification action helpers."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

CAPTCHA_CHALLENGE_KEYWORDS: tuple[str, ...] = (
    "captcha",
    "recaptcha",
    "hcaptcha",
    "turnstile",
    "prove you are human",
    "i'm not a robot",
    "i am not a robot",
    "type the characters as shown",
    "characters as shown above",
    "enter the characters shown",
    "verify you are human",
    "verify that you are human",
    "verify that you're a real person",
    "verify that you are a real person",
    "security challenge",
    "security check",
)
IMAGE_TEXT_CAPTCHA_KEYWORDS: tuple[str, ...] = (
    "type the characters as shown",
    "characters as shown above",
    "enter the characters shown",
)
IMAGE_COORDINATE_CAPTCHA_KEYWORDS: tuple[str, ...] = (
    "select all images",
    "select all squares",
    "click verify once",
    "click verify",
)


def normalize_captcha_prompt_text(text: str | None) -> str:
    """Normalize page text for stable keyword matching."""

    return " ".join(str(text or "").casefold().split())


def contains_captcha_keyword(
    text: str | None,
    keywords: Sequence[str],
) -> bool:
    """Return whether normalized text contains one of the supplied keywords."""

    normalized_text = normalize_captcha_prompt_text(text)
    return any(
        normalize_captcha_prompt_text(keyword) in normalized_text
        for keyword in keywords
    )


def classify_captcha_challenge(
    text: str | None,
    *,
    keywords: Sequence[str] = CAPTCHA_CHALLENGE_KEYWORDS,
) -> bool:
    """Return whether text indicates a CAPTCHA or human-verification challenge."""

    return contains_captcha_keyword(text, keywords)


def classify_human_verification(
    text: str | None,
    *,
    keywords: Sequence[str] = CAPTCHA_CHALLENGE_KEYWORDS,
) -> bool:
    """Alias for CAPTCHA-style human-verification detection."""

    return classify_captcha_challenge(text, keywords=keywords)


def classify_image_text_captcha(
    text: str | None,
    *,
    keywords: Sequence[str] = IMAGE_TEXT_CAPTCHA_KEYWORDS,
) -> bool:
    """Return whether text indicates an image/text-answer CAPTCHA."""

    return classify_captcha_challenge(text, keywords=keywords)


def classify_image_coordinate_captcha(
    text: str | None,
    *,
    keywords: Sequence[str] = IMAGE_COORDINATE_CAPTCHA_KEYWORDS,
) -> bool:
    """Return whether text indicates an image-click CAPTCHA."""

    return classify_captcha_challenge(text, keywords=keywords)


def solve_image_captcha(
    image_data: bytes,
    *,
    backend: str = "browser",
    captcha_solver_factory: Callable[..., Any] | None = None,
    **solver_kwargs: Any,
) -> str:
    """Solve an image CAPTCHA through Humanoid's configured solver backend."""

    if not image_data:
        raise ValueError("image_data is required.")
    if captcha_solver_factory is None:
        from humanoid.captcha_solver import CaptchaSolver

        captcha_solver_factory = CaptchaSolver
    solver = captcha_solver_factory(backend, **solver_kwargs)
    return str(solver.solve_captcha(image_data))
