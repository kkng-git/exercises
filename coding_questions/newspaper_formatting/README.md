# LEFT/RIGHT Newspaper Formatting

Given `paragraphs` of text portions, one `LEFT` or `RIGHT` alignment per
paragraph, and a content width, greedily wrap complete portions in order using
one space between portions. Pad each line on the required side, surround every
line with `*` side borders, and add top and bottom borders of `width + 2`
asterisks. Each paragraph starts on a new line. Never center text.

## Function

```python
formatNewspaper(paragraphs, aligns, width)
```

## Input

`paragraphs`, `aligns` containing only `LEFT` or `RIGHT`, and `width`.

## Output

An array of bordered newspaper lines.

## Local assessment files

Write your Python solution in `solution.py` and run the supplied test cases
with:

```bash
python3 -m unittest -v test_solution.py
```

To run one test:

```bash
python3 test_solution.py --test test_exact_width_line_has_no_padding
```
