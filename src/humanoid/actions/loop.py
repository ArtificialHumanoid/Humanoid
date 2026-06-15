"""Classification-action-classification loop helpers."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from humanoid.actions.types import (
    ActionChooser,
    ActionExecutor,
    ActionRequest,
    ActionResult,
    PageClassifier,
    PageSnapshot,
)


@dataclass(frozen=True)
class ActionLoopStep:
    """One classified action step."""

    index: int
    state: str
    action: ActionRequest
    result: ActionResult


@dataclass(frozen=True)
class ActionLoopResult:
    """Result of a bounded action loop."""

    status: str
    final_state: str
    final_snapshot: PageSnapshot
    steps: tuple[ActionLoopStep, ...]


def run_action_loop(
    initial_snapshot: PageSnapshot,
    *,
    classify: PageClassifier,
    choose_action: ActionChooser,
    execute_action: ActionExecutor,
    stop_when: Callable[[str, PageSnapshot], bool] | None = None,
    max_steps: int = 8,
) -> ActionLoopResult:
    """Run a bounded classify-act-reclassify loop."""

    if max_steps < 0:
        raise ValueError("max_steps must be non-negative.")

    snapshot = initial_snapshot
    steps: list[ActionLoopStep] = []
    state = classify(snapshot)
    for index in range(max_steps):
        if stop_when is not None and stop_when(state, snapshot):
            return ActionLoopResult("stopped", state, snapshot, tuple(steps))
        action = choose_action(state, snapshot)
        if action is None:
            return ActionLoopResult("no_action", state, snapshot, tuple(steps))
        result = execute_action(action, snapshot)
        steps.append(ActionLoopStep(index, state, action, result))
        if result.page is not None:
            snapshot = result.page
        state = classify(snapshot)

    if stop_when is not None and stop_when(state, snapshot):
        return ActionLoopResult("stopped", state, snapshot, tuple(steps))
    return ActionLoopResult("max_steps_reached", state, snapshot, tuple(steps))
