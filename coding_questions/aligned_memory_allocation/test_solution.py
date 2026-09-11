"""Public tests for the Aligned Memory Allocation assessment."""

import argparse
import sys
import unittest

from solution import processMemory


class ProcessMemoryTests(unittest.TestCase):
    def test_allocate_release_and_reuse_memory(self) -> None:
        memory = [0] * 16
        queries = [
            [0, 4],
            [0, 4],
            [1, 1],
            [0, 8],
            [1, 2],
            [1, 3],
        ]

        self.assertEqual(processMemory(memory, queries), [0, 8, 4, 0, 4, 8])
        self.assertEqual(memory, [0] * 16)

    def test_rejects_unaligned_free_space(self) -> None:
        memory = [1] + [0] * 7 + [1] * 8

        self.assertEqual(processMemory(memory, [[0, 4]]), [-1])
        self.assertEqual(memory, [1] + [0] * 7 + [1] * 8)

    def test_chooses_leftmost_valid_aligned_start(self) -> None:
        memory = [0, 0, 1, 0, 0, 0, 0, 0] + [0] * 8

        self.assertEqual(processMemory(memory, [[0, 4]]), [8])
        self.assertEqual(memory[8:12], [1, 1, 1, 1])

    def test_allocation_can_cross_an_alignment_boundary(self) -> None:
        memory = [0] * 24

        self.assertEqual(processMemory(memory, [[0, 10], [0, 6]]), [0, 16])

    def test_failed_allocation_does_not_consume_an_id(self) -> None:
        memory = [0] * 8
        queries = [[0, 9], [0, 4], [1, 1]]

        self.assertEqual(processMemory(memory, queries), [-1, 0, 4])
        self.assertEqual(memory, [0] * 8)

    def test_unknown_and_repeated_releases_return_zero(self) -> None:
        memory = [0] * 8
        queries = [[1, 1], [0, 3], [1, 1], [1, 1]]

        self.assertEqual(processMemory(memory, queries), [0, 0, 3, 0])
        self.assertEqual(memory, [0] * 8)

    def test_initially_occupied_cells_are_never_owned(self) -> None:
        memory = [1] + [0] * 15
        queries = [[0, 1], [1, 1]]

        self.assertEqual(processMemory(memory, queries), [8, 1])
        self.assertEqual(memory, [1] + [0] * 15)


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
        test_name = f"ProcessMemoryTests.{test_name}"

    loader = unittest.defaultTestLoader
    if test_name:
        suite = loader.loadTestsFromName(test_name, sys.modules[__name__])
    else:
        suite = loader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
