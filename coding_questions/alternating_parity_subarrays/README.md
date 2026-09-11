# Alternating-Parity Subarrays

Given an integer array `values`, count all contiguous subarrays in which every
pair of adjacent elements has different parity. A single-element subarray is
valid.

## Function

```python
countAlternatingParitySubarrays(values)
```

## Input

`values`, an array of integers.

## Output

The total number of valid contiguous subarrays.

## Example

For `values = [1, 2, 3]`, the output is `6`.

## Local assessment files

Write your Python solution in `solution.py` and run the supplied test cases
with:

```bash
python3 -m unittest -v test_solution.py
```

To run one test:

```bash
python3 test_solution.py --test test_single_element
```
