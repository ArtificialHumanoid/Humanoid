from __future__ import annotations

import time
from typing import Any, ClassVar
from unittest import TestCase

from test_server import Response, TestServer

from humanoid.captcha_solver import CaptchaSolver, error

# These timings means the solver will do only
# one attempt to submit captcha and
# one attempt to receive solution
# Assuming the network timeout is greater than
# submiting/recognition delays
TESTING_TIME_PARAMS: dict[str, float] = {
    "submiting_time": 0.1,
    "submiting_delay": 0.2,
    "recognition_time": 0.1,
    "recognition_delay": 0.2,
}
TEST_SERVER_HOST = "127.0.0.1"


class BaseSolverTestCase(TestCase):
    server: ClassVar[TestServer]

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = TestServer(address=TEST_SERVER_HOST)
        cls.server.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.stop()

    def setUp(self) -> None:
        self.server.reset()


class AntigateTestCase(BaseSolverTestCase):
    solver: CaptchaSolver

    def setUp(self) -> None:
        super().setUp()
        self.solver = self.create_solver()

    def create_solver(self, **kwargs: Any) -> CaptchaSolver:
        config: dict[str, Any] = {
            "service_url": self.server.get_url(),
            "api_key": "does not matter",
        }
        config.update(kwargs)
        return CaptchaSolver("antigate", **config)

    def test_post_data(self) -> None:
        data = b"foo"
        res = self.solver.backend.get_submit_captcha_request_data(data)
        assert res["post_data"] is not None
        body = res["post_data"]["body"]

        self.assertTrue(isinstance(body, str))

    def test_antigate_decoded(self) -> None:
        self.server.add_response(Response(data=b"OK|captcha_id"))
        self.server.add_response(Response(data=b"OK|decoded_captcha"))
        self.assertEqual(self.solver.solve_captcha(b"image_data"), "decoded_captcha")

    def test_check_solution_url_encodes_query_parameters(self) -> None:
        solver = self.create_solver(api_key="key with space")
        request_data = solver.backend.get_check_solution_request_data("captcha/id")
        expected_url = (
            f"{self.server.get_url()}/res.php?"
            "key=key+with+space&action=get&id=captcha%2Fid"
        )
        assert request_data == {"url": expected_url, "post_data": None}

    def test_antigate_no_slot_available(self) -> None:
        self.server.add_response(Response(data=b"ERROR_NO_SLOT_AVAILABLE"), count=-1)
        with self.assertRaises(error.SolutionTimeoutError):
            self.solver.solve_captcha(b"image_data", **TESTING_TIME_PARAMS)

    def test_antigate_zero_balance(self) -> None:
        self.server.add_response(Response(data=b"ERROR_ZERO_BALANCE"))
        self.assertRaises(error.BalanceTooLow, self.solver.solve_captcha, b"image_data")

    def test_antigate_unknown_error(self) -> None:
        self.server.add_response(Response(data=b"UNKNOWN_ERROR"))
        self.assertRaises(
            error.CaptchaServiceError, self.solver.solve_captcha, b"image_data"
        )

    def test_antigate_unknown_code(self) -> None:
        self.server.add_response(Response(status=404))
        self.assertRaises(
            error.CaptchaServiceError, self.solver.solve_captcha, b"image_data"
        )

    def test_solution_timeout_error(self) -> None:
        self.server.add_response(Response(data=b"OK|captcha_id"))
        self.server.add_response(Response(data=b"CAPCHA_NOT_READY"))
        with self.assertRaises(error.SolutionTimeoutError):
            self.solver.solve_captcha(b"image_data", **TESTING_TIME_PARAMS)

    def test_solution_unknown_error(self) -> None:
        self.server.add_response(Response(data=b"OK|captcha_id"))
        self.server.add_response(Response(data=b"UNKONWN_ERROR"))
        with self.assertRaises(error.CaptchaServiceError):
            self.solver.solve_captcha(b"image_data", **TESTING_TIME_PARAMS)

    def test_solution_unknown_code(self) -> None:
        self.server.add_response(Response(data=b"OK|captcha_id"))
        self.server.add_response(Response(data=b"OK|solution", status=500))
        with self.assertRaises(error.CaptchaServiceError):
            self.solver.solve_captcha(b"image_data", **TESTING_TIME_PARAMS)

    def test_network_error_while_sending_captcha(self) -> None:
        self.server.add_response(Response(data=b"that would be timeout", sleep=0.5))
        self.server.add_response(Response(data=b"OK|captcha_id"))
        self.server.add_response(Response(data=b"OK|solution"))

        solver = self.create_solver()
        solver.setup_network_config(timeout=0.4)
        solver.solve_captcha(
            b"image_data",
            submiting_time=2,
            submiting_delay=0,
            recognition_time=0,
            recognition_delay=0,
        )

    def test_network_error_while_receiving_solution(self) -> None:
        class Callback:
            def __init__(self) -> None:
                self.step = 0

            def __call__(self) -> dict[str, object]:
                self.step += 1
                if self.step == 1:
                    return {
                        "type": "response",
                        "data": b"OK|captcha_id",
                    }
                if self.step in {2, 3, 4}:
                    time.sleep(0.2)
                    return {
                        "type": "response",
                        "data": b"that will be timeout",
                    }
                return {
                    "type": "response",
                    "data": b"OK|solution",
                }

        solver = self.create_solver()
        solver.setup_network_config(timeout=0.1)
        self.server.add_response(Response(callback=Callback()), count=-1)
        solution = solver.solve_captcha(
            b"image_data",
            submiting_time=0,
            submiting_delay=0,
            recognition_time=1,
            recognition_delay=0.09,
        )
        assert solution == "solution"
