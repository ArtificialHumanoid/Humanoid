from __future__ import annotations

from typing import Any
from unittest import TestCase

from humanoid.actions import browser, captcha, click, safety, spaces
from humanoid.actions.loop import run_action_loop
from humanoid.actions.spaces import Literal
from humanoid.actions.types import ActionRequest, ActionResult, PageSnapshot
from humanoid.actions.internet_search import HTTPAdapter as ActionsHTTPAdapter
from humanoid.actions.internet_search.google import SearchResult as ActionsSearchResult


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

    def test_browser_action_builders_validate_and_normalize_payloads(self) -> None:
        navigate = browser.navigate(" https://example.com/login ")
        typed = browser.type_text("masked-value", selector="#entry", secret=True)

        self.assertEqual(navigate.name, browser.BROWSER_NAVIGATE)
        self.assertEqual(navigate.parameters["url"], "https://example.com/login")
        self.assertEqual(typed.name, browser.BROWSER_TYPE_TEXT)
        self.assertEqual(typed.parameters["selector"], "#entry")
        self.assertTrue(typed.parameters["secret"])

        with self.assertRaises(ValueError):
            browser.navigate("")
        with self.assertRaises(ValueError):
            browser.evaluate("")
        with self.assertRaises(ValueError):
            browser.wait(-0.01)
        with self.assertRaises(ValueError):
            browser.click(x=1)

    def test_click_adapter_keeps_browser_click_request_available(self) -> None:
        action = click.click(text="Continue")

        self.assertEqual(action.name, browser.BROWSER_CLICK)
        self.assertEqual(action.parameters["text"], "Continue")

    def test_click_adapter_delegates_debug_page_click_to_screen_helper(self) -> None:
        calls: list[dict[str, Any]] = []

        class ScreenClick:
            @staticmethod
            def advance_debug_page_click(
                debug_url: str,
                expected_state_description: str,
                **kwargs: Any,
            ) -> dict[str, Any]:
                calls.append(
                    {
                        "debug_url": debug_url,
                        "expected_state_description": expected_state_description,
                        **kwargs,
                    }
                )
                return {"status": "advanced", "secret_values_returned": False}

        result = click.advance_debug_page_click(
            "debug-page",
            "next page",
            text="Sign in",
            screen_click=ScreenClick,
        )

        self.assertEqual(result["status"], "advanced")
        self.assertFalse(result["secret_values_returned"])
        self.assertEqual(calls[0]["text"], "Sign in")

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

        def choose_action(state: str, snapshot: PageSnapshot) -> ActionRequest | None:
            if state == "start":
                return browser.navigate("https://example.com")
            return None

        def execute_action(
            action: ActionRequest,
            snapshot: PageSnapshot,
        ) -> ActionResult:
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

    def test_action_loop_returns_no_action_when_chooser_stops(self) -> None:
        snapshot = PageSnapshot(metadata={"state": "idle"})

        result = run_action_loop(
            snapshot,
            classify=lambda page: str(page.metadata["state"]),
            choose_action=lambda _state, _snapshot: None,
            execute_action=lambda _action, _snapshot: ActionResult("unexpected"),
        )

        self.assertEqual(result.status, "no_action")
        self.assertEqual(result.final_state, "idle")
        self.assertEqual(result.final_snapshot, snapshot)
        self.assertEqual(result.steps, ())

    def test_action_loop_reports_max_steps_when_not_stopped(self) -> None:
        snapshot = PageSnapshot(metadata={"state": "repeat"})

        result = run_action_loop(
            snapshot,
            classify=lambda page: str(page.metadata["state"]),
            choose_action=lambda _state, _snapshot: browser.wait(0),
            execute_action=lambda action, page: ActionResult(
                "waited",
                action=action.name,
                page=page,
            ),
            max_steps=2,
        )

        self.assertEqual(result.status, "max_steps_reached")
        self.assertEqual(result.final_state, "repeat")
        self.assertEqual(len(result.steps), 2)
        self.assertEqual([step.index for step in result.steps], [0, 1])

    def test_safety_marks_status_results_as_secret_free(self) -> None:
        result = safety.status_result("ok", metadata={"page_id": "abc"})

        self.assertFalse(result.secret_values_returned)
        self.assertFalse(result.metadata["secret_values_returned"])
        self.assertEqual(result.metadata["page_id"], "abc")

    def test_safety_redacts_sensitive_mapping_keys(self) -> None:
        redacted = safety.redact_sensitive_mapping(
            {
                "username": "user@example.com",
                "api_key": "hide-this",
                "refreshToken": "hide-this-too",
            }
        )

        self.assertEqual(redacted["username"], "user@example.com")
        self.assertEqual(redacted["api_key"], "[redacted]")
        self.assertEqual(redacted["refreshToken"], "[redacted]")

    def test_internet_search_exports_resolve_from_actions_package(self) -> None:
        self.assertEqual(ActionsHTTPAdapter.__name__, "HTTPAdapter")
        self.assertEqual(ActionsSearchResult.__name__, "SearchResult")
