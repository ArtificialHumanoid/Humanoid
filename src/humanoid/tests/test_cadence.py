from __future__ import annotations

from typing import Iterator, List, Tuple
from unittest import TestCase
from unittest.mock import patch

from humanoid.mimicry.cadence import random_sleep_between_lines


class CadenceTestCase(TestCase):
    def test_sleeps_between_executed_lines(self) -> None:
        bounds: List[Tuple[float, float]] = []
        durations: List[float] = []

        def fake_uniform(minimum_seconds: float, maximum_seconds: float) -> float:
            bounds.append((minimum_seconds, maximum_seconds))
            return 0.1

        def fake_sleep(duration: float) -> None:
            durations.append(duration)

        @random_sleep_between_lines()
        def sample() -> int:
            value = 1
            value += 2
            if value:
                value += 3
            return value

        with patch("humanoid.mimicry.cadence.uniform", side_effect=fake_uniform):
            with patch("humanoid.mimicry.cadence.sleep", side_effect=fake_sleep):
                result = sample()

        self.assertEqual(result, 6)
        self.assertEqual(sample.__name__, "sample")
        self.assertEqual(bounds, [(0.05, 0.25)] * 4)
        self.assertEqual(durations, [0.1] * 4)

    def test_repeats_sleep_for_loop_line_events(self) -> None:
        durations: List[float] = []

        def fake_sleep(duration: float) -> None:
            durations.append(duration)

        @random_sleep_between_lines(0, 0)
        def sample() -> int:
            total = 0
            for value in range(2):
                total += value
            return total

        with patch("humanoid.mimicry.cadence.uniform", return_value=0.0):
            with patch("humanoid.mimicry.cadence.sleep", side_effect=fake_sleep):
                self.assertEqual(sample(), 1)

        self.assertGreater(len(durations), 3)

    def test_does_not_instrument_nested_calls(self) -> None:
        durations: List[float] = []

        def fake_sleep(duration: float) -> None:
            durations.append(duration)

        def helper() -> int:
            value = 1
            value += 1
            return value

        @random_sleep_between_lines(0, 0)
        def sample() -> int:
            value = helper()
            return value

        with patch("humanoid.mimicry.cadence.uniform", return_value=0.0):
            with patch("humanoid.mimicry.cadence.sleep", side_effect=fake_sleep):
                self.assertEqual(sample(), 2)

        self.assertEqual(len(durations), 1)

    def test_rejects_invalid_delay_bounds(self) -> None:
        with self.assertRaises(ValueError):
            random_sleep_between_lines(-0.01, 0.25)
        with self.assertRaises(ValueError):
            random_sleep_between_lines(0.05, -0.25)
        with self.assertRaises(ValueError):
            random_sleep_between_lines(0.25, 0.05)

    def test_rejects_non_synchronous_functions(self) -> None:
        def generator() -> Iterator[int]:
            yield 1

        async def asynchronous() -> int:
            return 1

        with self.assertRaises(TypeError):
            random_sleep_between_lines()(generator)
        with self.assertRaises(TypeError):
            random_sleep_between_lines()(asynchronous)
