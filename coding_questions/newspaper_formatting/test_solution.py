"""Public tests for the LEFT/RIGHT Newspaper Formatting assessment."""

import unittest

from solution import formatNewspaper


class FormatNewspaperTests(unittest.TestCase):
    def test_mixed_alignment_and_wrapping(self) -> None:
        paragraphs = [
            ["hello", "world"],
            ["right", "aligned", "text"],
        ]
        aligns = ["LEFT", "RIGHT"]

        self.assertEqual(
            formatNewspaper(paragraphs, aligns, 12),
            [
                "**************",
                "*hello world *",
                "*       right*",
                "*aligned text*",
                "**************",
            ],
        )

    def test_wraps_complete_portions_greedily(self) -> None:
        self.assertEqual(
            formatNewspaper([["aa", "b", "cc"]], ["LEFT"], 6),
            ["********", "*aa b  *", "*cc    *", "********"],
        )

    def test_paragraphs_never_share_a_line(self) -> None:
        self.assertEqual(
            formatNewspaper([["a"], ["b"]], ["LEFT", "LEFT"], 5),
            ["*******", "*a    *", "*b    *", "*******"],
        )

    def test_right_alignment_pads_on_the_left(self) -> None:
        self.assertEqual(
            formatNewspaper([["abc"], ["d", "e"]], ["RIGHT", "RIGHT"], 5),
            ["*******", "*  abc*", "*  d e*", "*******"],
        )

    def test_exact_width_line_has_no_padding(self) -> None:
        self.assertEqual(
            formatNewspaper([["ab", "cd"]], ["RIGHT"], 5),
            ["*******", "*ab cd*", "*******"],
        )

    def test_single_character_width(self) -> None:
        self.assertEqual(
            formatNewspaper([["a", "b"]], ["LEFT"], 1),
            ["***", "*a*", "*b*", "***"],
        )

    def test_each_paragraph_uses_its_own_alignment(self) -> None:
        self.assertEqual(
            formatNewspaper(
                [["left", "side"], ["right", "side"]],
                ["LEFT", "RIGHT"],
                10,
            ),
            ["************", "*left side *", "*right side*", "************"],
        )


if __name__ == "__main__":
    unittest.main()
