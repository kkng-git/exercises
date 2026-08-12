# Aligned Memory Allocation

You are given a binary memory array, where `0` is free and `1` is occupied, and
a list of queries. For `[0, x]`, find the leftmost free run of `x` cells whose
start index is a multiple of `8`. Mark it occupied and return its start, or
return `-1` if none exists. Each successful allocation receives the next
allocation ID; failed allocations do not consume an ID.

For `[1, id]`, release all cells owned by that successful-allocation ID and
return the number of cells released.

## Function

```python
processMemory(memory, queries)
```

## Input

- `memory`, an array of `0` and `1`
- `queries`, an array of `[operation, value]` pairs

## Output

An integer array containing the result of each query.

## Local assessment files

Write your Python solution in `solution.py` and run the supplied test cases
with:

```bash
python3 -m unittest -v test_solution.py
```
