from __future__ import annotations

from typing import Any
from unittest import TestCase
from unittest.mock import patch

from humanoid.captcha_solver import CaptchaSolver


class BrowserTestCase(TestCase):
    wb_patcher: Any
    mock_wb_open: Any
    raw_input_patcher: Any
    mock_raw_input: Any
    solver: CaptchaSolver

    def setUp(self) -> None:
        self.solver = CaptchaSolver("browser")
        self.wb_patcher = patch("webbrowser.open")
        self.mock_wb_open = self.wb_patcher.start()
        self.raw_input_patcher = patch("humanoid.captcha_solver.backend.browser.input")
        self.mock_raw_input = self.raw_input_patcher.start()

    def tearDown(self) -> None:
        self.wb_patcher.stop()
        self.raw_input_patcher.stop()

    def test_captcha_decoded(self) -> None:
        self.mock_wb_open.return_value = None
        self.mock_raw_input.return_value = "decoded_captcha"

        self.assertEqual(self.solver.solve_captcha(b"image_data"), "decoded_captcha")
