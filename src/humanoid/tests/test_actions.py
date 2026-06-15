from __future__ import annotations

from unittest import TestCase

from humanoid.actions import browser, captcha, safety, spaces
from humanoid.actions.loop import run_action_loop
from humanoid.actions.types import ActionResult, PageSnapshot
from humanoid.actions.internet_search import HTTPAdapter as ActionsHTTPAdapter
from humanoid.actions.internet_search.google import SearchResult as ActionsSearchResult
from utilities.meta.types_management import Literal


class ActionsTestCase(TestCase):
    def test_captcha_classifiers_detect_common_challenges(self) -> None:
        text = (
            "Security check: select all images with traffic lights, "
            "then click verify."
        )

        self.assertTrue(captcha.classify_captcha_challenge(text))
        self.assertTrue(captcha.classify_image_coordinate_captcha(text))
        self.assertFalse(captcha.classify_image_text_captcha(text))

    def test_browser_click_requires_a_target(self) -> None:
        with self.assertRaises(ValueError):
            browser.click()

        action = browser.click(selector="button[type=submit]")

        self.assertEqual(action.name, browser.BROWSER_CLICK)
        self.assertEqual(action.parameters["selector"], "button[type=submit]")

    def test_action_space_literals_are_named(self) -> None:
        expected_literals = (
            (spaces.Actions.wait, "wait", "Actions.wait"),
            (spaces.Actions.type, "type", "Actions.type"),
            (spaces.Actions.Mouse.Click.left, "left", "Actions.Mouse.Click.left"),
            (spaces.Actions.Mouse.Click.right, "right", "Actions.Mouse.Click.right"),
            (spaces.Actions.Mouse.Click.middle, "middle", "Actions.Mouse.Click.middle"),
            (spaces.Actions.Mouse.position, "position", "Actions.Mouse.position"),
            (spaces.Actions.Mouse.scroll, "scroll", "Actions.Mouse.scroll"),
            (spaces.Actions.Run.os, "os", "Actions.Run.os"),
            (spaces.Actions.Run.python, "python", "Actions.Run.python"),
        )

        for literal, value, qualified_name in expected_literals:
            with self.subTest(qualified_name=qualified_name):
                self.assertIsInstance(literal, Literal)
                self.assertEqual(str(literal), value)
                self.assertEqual(literal.value, value)
                self.assertEqual(literal, value)
                self.assertEqual(literal.qualified_name, qualified_name)

    def test_action_loop_reclassifies_after_each_action(self) -> None:
        initial_snapshot = PageSnapshot(metadata={"state": "start"})

        def classify(snapshot: PageSnapshot) -> str:
            return str(snapshot.metadata.get("state") or "unknown")

        def choose_action(state: str, _snapshot: PageSnapshot):
            if state == "start":
                return browser.navigate("https://example.com")
            return None

        def execute_action(action, _snapshot: PageSnapshot) -> ActionResult:
            return ActionResult(
                "navigated",
                action=action.name,
                page=PageSnapshot(
                    url=action.parameters["url"],
                    metadata={"state": "done"},
                ),
            )

        result = run_action_loop(
            initial_snapshot,
            classify=classify,
            choose_action=choose_action,
            execute_action=execute_action,
            stop_when=lambda state, _snapshot: state == "done",
        )

        self.assertEqual(result.status, "stopped")
        self.assertEqual(result.final_state, "done")
        self.assertEqual(len(result.steps), 1)

    def test_safety_marks_status_results_as_secret_free(self) -> None:
        result = safety.status_result("ok", metadata={"page_id": "abc"})

        self.assertFalse(result.secret_values_returned)
        self.assertFalse(result.metadata["secret_values_returned"])
        self.assertEqual(result.metadata["page_id"], "abc")

    def test_internet_search_exports_resolve_from_actions_package(self) -> None:
        self.assertEqual(ActionsHTTPAdapter.__name__, "HTTPAdapter")
        self.assertEqual(ActionsSearchResult.__name__, "SearchResult")
