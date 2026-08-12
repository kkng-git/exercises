# Aligned Memory Allocation

**Difficulty:** Medium  
**Suggested time:** 45 minutes

## Problem

You are given a binary array `memory` representing a contiguous region of
memory:

- `0` means the cell is free.
- `1` means the cell is occupied.

You are also given a list of queries. Process the queries in order while
mutating `memory` to reflect successful allocations and releases.

Implement:

```python
def processMemory(memory: list[int], queries: list[list[int]]) -> list[int]:
```

The function must return one integer result for every query.

## Query types

### Allocate: `[0, size]`

Find the leftmost sequence of `size` consecutive free cells whose starting
index is a multiple of `8`.

More precisely, find the smallest index `start` for which all of the following
are true:

1. `start % 8 == 0`
2. `start + size <= len(memory)`
3. Every cell from `memory[start]` through
   `memory[start + size - 1]` is `0`

If a valid sequence exists:

- Change all cells in the sequence to `1`.
- Associate the sequence with the next allocation ID.
- Return `start`.

Allocation IDs begin at `1` and increase by one after each successful
allocation. A failed allocation does **not** consume an ID.

If no valid sequence exists, leave `memory` unchanged and return `-1`.

> Alignment applies only to the starting index. The allocation size does not
> need to be a multiple of `8`, and an allocation may cross an 8-cell boundary.

### Release: `[1, allocation_id]`

If `allocation_id` belongs to an active successful allocation:

- Change every cell owned by that allocation to `0`.
- Retire the allocation ID so it cannot be released again.
- Return the number of cells released.

If the ID is unknown or has already been released, leave `memory` unchanged
and return `0`.

Cells that were occupied in the initial `memory` array do not belong to an
allocation and must never be released by a query.

## Constraints

- `1 <= len(memory) <= 1_000`
- `memory[i]` is either `0` or `1`
- `1 <= len(queries) <= 1_000`
- Every query contains exactly two integers
- `queries[i][0]` is either `0` or `1`
- For an allocation query, `queries[i][1] >= 1`
- For a release query, `queries[i][1] >= 1`

## Example 1

```python
memory = [0] * 16
queries = [
    [0, 4],
    [0, 4],
    [1, 1],
    [0, 8],
    [1, 2],
    [1, 3],
]

processMemory(memory, queries) == [0, 8, 4, 0, 4, 8]
```

Explanation:

1. Four cells are allocated at index `0` with ID `1`.
2. Index `0` is unavailable, so four cells are allocated at index `8` with
   ID `2`.
3. Releasing ID `1` frees four cells.
4. Eight cells can now be allocated at index `0` with ID `3`.
5. Releasing ID `2` frees four cells.
6. Releasing ID `3` frees eight cells.

## Example 2

```python
memory = [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
queries = [[0, 4]]

processMemory(memory, queries) == [-1]
```

There are seven consecutive free cells beginning at index `1`, but index `1`
is not aligned to a multiple of `8`.

## Example 3

```python
memory = [0] * 8
queries = [
    [0, 9],  # fails and does not consume ID 1
    [0, 4],  # succeeds with ID 1
    [1, 1],
]

processMemory(memory, queries) == [-1, 0, 4]
```

## Public test cases

The included tests cover:

- Processing multiple queries and returning one result per query
- Choosing the leftmost aligned location
- Rejecting unaligned free space
- Allocations that cross an 8-cell boundary
- Failed allocations not consuming IDs
- Releasing unknown and already-released IDs
- Preserving cells that were occupied initially

Run them from this directory with:

```bash
python3 -m unittest -v test_solution.py
```

The starter implementation intentionally raises `NotImplementedError`, so the
tests will fail until `processMemory` is implemented.

