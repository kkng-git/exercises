"""Public tests for the Drone Delivery assessment."""

import argparse
import sys
import unittest

from solution import droneDelivery


class DroneDeliveryTests(unittest.TestCase):
    def test_example_with_unsorted_stations(self) -> None:
        self.assertEqual(droneDelivery(23, [7, 4, 14]), 4)

    def test_no_stations(self) -> None:
        self.assertEqual(droneDelivery(25, []), 25)

    def test_station_chain_requires_no_walking(self) -> None:
        self.assertEqual(droneDelivery(25, [20, 0, 10]), 0)

    def test_drone_skips_stations_behind_new_position(self) -> None:
        self.assertEqual(droneDelivery(30, [3, 5, 13, 22]), 10)

    def test_walks_between_gaps_in_drone_coverage(self) -> None:
        self.assertEqual(droneDelivery(30, [2, 15, 27]), 7)

    def test_drone_stops_at_target_before_ten_units(self) -> None:
        self.assertEqual(droneDelivery(8, [0]), 0)

    def test_station_at_target_does_not_reduce_walking(self) -> None:
        self.assertEqual(droneDelivery(8, [8]), 8)


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
        test_name = f"DroneDeliveryTests.{test_name}"

    loader = unittest.defaultTestLoader
    if test_name:
        suite = loader.loadTestsFromName(test_name, sys.modules[__name__])
    else:
        suite = loader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
