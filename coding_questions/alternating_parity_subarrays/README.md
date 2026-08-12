# Alternating-Parity Subarrays

**Difficulty:** Easy/Medium  
**Suggested time:** 30 minutes

## Problem

Given an integer array `values`, count the non-empty contiguous subarrays in
which every pair of adjacent elements has different parity.

Two integers have different parity when one is even and the other is odd. A
single-element subarray is always valid because it has no adjacent pair that
violates the rule.

Implement:

```python
def countAlternatingParitySubarrays(values: list[int]) -> int:
```

Return the total number of valid contiguous subarrays.

## Definitions

- A **subarray** consists of consecutive elements from the original array.
- Subarrays with the same values but different index ranges are counted
  separately.
- `0` is even.
- Negative integers follow the usual parity rules; for example, `-3` is odd
  and `-4` is even.

## Constraints

- `1 <= len(values) <= 100_000`
- `-10**9 <= values[i] <= 10**9`
- The answer fits in a signed 64-bit integer.

## Example 1

```python
values = [1, 2, 3]

countAlternatingParitySubarrays(values) == 6
```

All six non-empty subarrays are valid:

```text
[1], [2], [3], [1, 2], [2, 3], [1, 2, 3]
```

## Example 2

```python
values = [2, 4, 6]

countAlternatingParitySubarrays(values) == 3
```

Only the three single-element subarrays are valid.

## Example 3

```python
values = [1, 2, 4, 5]

countAlternatingParitySubarrays(values) == 6
```

The valid subarrays are the four single elements plus `[1, 2]` and `[4, 5]`.

## Performance target

Aim for:

- `O(n)` time
- `O(1)` auxiliary space

## Public tests

The included tests cover single-element input, fully alternating input,
same-parity input, parity breaks, zero, and negative values.

Run them from this directory with:

```bash
python3 -m unittest -v test_solution.py
```

The starter implementation intentionally raises `NotImplementedError`, so the
tests will fail until the function is implemented.

