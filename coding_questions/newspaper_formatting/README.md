# LEFT/RIGHT Newspaper Formatting

**Difficulty:** Medium  
**Suggested time:** 45 minutes

## Problem

You are given:

- `paragraphs`, a list of paragraphs, where each paragraph is a list of text
  portions
- `aligns`, containing one alignment (`"LEFT"` or `"RIGHT"`) for each
  paragraph
- `width`, the content width of the newspaper

Format the paragraphs as a bordered newspaper. Return the finished newspaper
as a list of strings, one string per output line.

Implement:

```python
def formatNewspaper(
    paragraphs: list[list[str]],
    aligns: list[str],
    width: int,
) -> list[str]:
```

## Wrapping rules

Process each paragraph's portions from left to right:

1. Place as many complete portions as possible on the current line.
2. Separate adjacent portions on the same line with exactly one space.
3. If adding the next portion and its separating space would make the line
   longer than `width`, begin a new line with that portion.
4. Never split a portion across lines.
5. Every paragraph begins on a new output line. Text from different paragraphs
   is never combined, even when the previous paragraph's final line has room.
6. Do not insert blank lines between paragraphs.

Wrapping is greedy: a portion must be placed on the current line whenever it
fits.

## Alignment and border rules

Each content line must contain exactly `width` characters before its side
borders are added.

- For `"LEFT"`, place padding spaces after the text.
- For `"RIGHT"`, place padding spaces before the text.
- Do not center text.
- Surround every content line with one `*` on each side.
- Add a top border and a bottom border, each containing exactly `width + 2`
  asterisks.

## Constraints

- `1 <= len(paragraphs) <= 1_000`
- `len(aligns) == len(paragraphs)`
- `aligns[i]` is either `"LEFT"` or `"RIGHT"`
- Every paragraph contains at least one portion
- Every portion is a non-empty string without leading or trailing whitespace
- `1 <= len(portion) <= width`
- `1 <= width <= 1_000`
- The total number of characters across all portions is at most `100_000`

## Example 1

```python
paragraphs = [
    ["hello", "world"],
    ["right", "aligned", "text"],
]
aligns = ["LEFT", "RIGHT"]
width = 12

formatNewspaper(paragraphs, aligns, width) == [
    "**************",
    "*hello world *",
    "*       right*",
    "*aligned text*",
    "**************",
]
```

`"hello world"` fits on one line and receives one trailing space. In the
second paragraph, `"right aligned"` would exceed the width, so `"right"`
forms a right-aligned line by itself. The remaining two portions exactly fill
the next line.

## Example 2

```python
paragraphs = [["aa", "b", "cc"]]
aligns = ["LEFT"]
width = 6

formatNewspaper(paragraphs, aligns, width) == [
    "********",
    "*aa b  *",
    "*cc    *",
    "********",
]
```

Although `"cc"` has only two characters, adding it to `"aa b"` would require
one separating space and produce seven characters. It therefore begins a new
line.

## Example 3

```python
paragraphs = [["a"], ["b"]]
aligns = ["LEFT", "LEFT"]
width = 5

formatNewspaper(paragraphs, aligns, width) == [
    "*******",
    "*a    *",
    "*b    *",
    "*******",
]
```

The two portions belong to different paragraphs, so they cannot share a line.

## Performance target

Aim for linear time in the total number of input and output characters.

## Public tests

The included tests cover greedy wrapping, exact-width lines, both alignments,
paragraph boundaries, minimum width, and multiple output lines.

Run them from this directory with:

```bash
python3 -m unittest -v test_solution.py
```

The starter implementation intentionally raises `NotImplementedError`, so the
tests will fail until the function is implemented.

