# Drone Delivery

**Difficulty:** Medium  
**Suggested time:** 35 minutes

## Problem

Cargo begins at position `0` on a number line and must reach `target`. Several
drone stations are located between position `0` and `target`.

Move the cargo according to this deterministic process:

1. Find the nearest drone station at or ahead of the cargo's current position.
2. Carry the cargo on foot to that station. This distance contributes to the
   answer.
3. The station's drone carries the cargo up to `10` units toward `target`.
4. Repeat until the cargo reaches `target`.

If there is no station at or ahead of the cargo's current position, carry the
cargo directly to `target` on foot.

Return only the total distance for which the cargo was carried on foot. Do not
include distance traveled by a drone.

Implement:

```python
def droneDelivery(target: int, stations: list[int]) -> int:
```

## Details

- The cargo always moves toward `target` and never moves backward.
- The station positions are not guaranteed to be sorted.
- "Nearest at or ahead" means the station with the smallest position greater
  than or equal to the cargo's current position.
- A station at the cargo's current position can be used with no additional
  walking distance.
- A drone moves the cargo to `min(current_position + 10, target)`.
- A station skipped over by a drone is then behind the cargo and cannot be
  used later.

## Constraints

- `1 <= target <= 10**9`
- `0 <= len(stations) <= 100_000`
- `0 <= stations[i] <= target`
- Station positions are unique.

## Example 1

```python
target = 23
stations = [7, 4, 14]

droneDelivery(target, stations) == 4
```

Explanation:

1. Walk from `0` to station `4`: walking distance is `4`.
2. The drone at `4` moves the cargo to `14`.
3. A station exists at `14`, so no walking is needed to reach it.
4. Its drone moves the cargo from `14` to `23`.

The total distance traveled on foot is `4`.

## Example 2

```python
target = 30
stations = [3, 5, 13, 22]

droneDelivery(target, stations) == 10
```

The cargo is carried on foot from `0` to `3`, then flown to `13`. It is flown
again from station `13` to `23`, skipping station `22`. With no usable station
remaining, it is carried the final `7` units on foot. The total is `3 + 7 = 10`.

## Example 3

```python
target = 25
stations = []

droneDelivery(target, stations) == 25
```

With no stations, the cargo travels the entire distance on foot.

## Performance target

Aim for `O(n log n)` time or better, where `n` is the number of stations.

## Public tests

The included tests cover unsorted stations, no stations, stations at the
current position, gaps between drone routes, skipped stations, and a final
partial drone trip.

Run them from this directory with:

```bash
python3 -m unittest -v test_solution.py
```

The starter implementation intentionally raises `NotImplementedError`, so the
tests will fail until the function is implemented.

