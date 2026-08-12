# Drone Delivery

Cargo starts at position 0 on a line. Repeatedly carry it on foot to the nearest
drone station at or ahead of its current position, then let the drone move it
up to 10 units toward `target`. If no usable station remains, carry it to
`target`. Return only the total distance the cargo travels on foot.

## Input/Output

- **[execution time limit]** 4 seconds (js)
- **[memory limit]** 1 GB
- **[input]** `target`, an integer
- **[input]** `stations`, an array of integers

`target`, the destination.

`stations`, an array of station positions.

- **[output]** integer

The total cargo-on-foot distance.

## Example

For `target = 23` and `stations = [7, 4, 14]`, the output is `4`.

## Local assessment files

Write your Python solution in `solution.py` and run the supplied test cases
with:

```bash
python3 -m unittest -v test_solution.py
```
