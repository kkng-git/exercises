"""Public tests for the Alternating-Parity Subarrays assessment."""

import argparse
import sys
import unittest

from solution import countAlternatingParitySubarrays


class CountAlternatingParitySubarraysTests(unittest.TestCase):
    def test_example_all_subarrays_are_valid(self) -> None:
        self.assertEqual(countAlternatingParitySubarrays([1, 2, 3]), 6)

    def test_only_single_element_subarrays_are_valid(self) -> None:
        self.assertEqual(countAlternatingParitySubarrays([2, 4, 6]), 3)

    def test_single_element(self) -> None:
        self.assertEqual(countAlternatingParitySubarrays([7]), 1)

    def test_parity_break_splits_alternating_runs(self) -> None:
        self.assertEqual(countAlternatingParitySubarrays([1, 2, 4, 5]), 6)

    def test_long_fully_alternating_array(self) -> None:
        self.assertEqual(countAlternatingParitySubarrays([2, 1, 4, 3, 6]), 15)

    def test_multiple_alternating_runs(self) -> None:
        self.assertEqual(countAlternatingParitySubarrays([1, 2, 3, 5, 6]), 9)

    def test_zero_and_negative_values(self) -> None:
        self.assertEqual(countAlternatingParitySubarrays([-3, 0, -1, 2]), 10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the public tests.")
    parser.add_argument(
        "--test",
        metavar="NAME",
        help="run one test method instead of the full suite",
    )
    args = parser.parse_args()

    test_name = args.test
    if test_name and "." not in test_name:
        test_name = f"CountAlternatingParitySubarraysTests.{test_name}"

    loader = unittest.defaultTestLoader
    if test_name:
        suite = loader.loadTestsFromName(test_name, sys.modules[__name__])
    else:
        suite = loader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
