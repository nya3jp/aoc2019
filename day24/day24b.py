import collections
from typing import Dict, Set, Tuple

Point = Tuple[int, int]
Level = Set[Point]
State = Dict[int, Level]


def simulate(state: State) -> State:
    lvmin = min(state.keys())
    lvmax = max(state.keys())
    newstate = collections.defaultdict(set)
    for lv in range(lvmin - 1, lvmax + 2):
        for i in range(5):
            for j in range(5):
                if i == 2 and j == 2:
                    continue
                cnt = 0
                # Up
                if i == 0:
                    cnt += 1 if (1, 2) in state[lv-1] else 0
                elif (i, j) == (3, 2):
                    cnt += sum(1 for k in range(5) if (4, k) in state[lv+1])
                else:
                    cnt += 1 if (i-1, j) in state[lv] else 0
                # Left
                if j == 0:
                    cnt += 1 if (2, 1) in state[lv-1] else 0
                elif (i, j) == (2, 3):
                    cnt += sum(1 for k in range(5) if (k, 4) in state[lv+1])
                else:
                    cnt += 1 if (i, j-1) in state[lv] else 0
                # Down
                if i == 4:
                    cnt += 1 if (3, 2) in state[lv-1] else 0
                elif (i, j) == (1, 2):
                    cnt += sum(1 for k in range(5) if (0, k) in state[lv+1])
                else:
                    cnt += 1 if (i+1, j) in state[lv] else 0
                # Right
                if j == 4:
                    cnt += 1 if (2, 3) in state[lv-1] else 0
                elif (i, j) == (2, 1):
                    cnt += sum(1 for k in range(5) if (k, 0) in state[lv+1])
                else:
                    cnt += 1 if (i, j+1) in state[lv] else 0
                if (i, j) in state[lv]:
                    if cnt == 1:
                        newstate[lv].add((i, j))
                else:
                    if cnt == 1 or cnt == 2:
                        newstate[lv].add((i, j))
    return newstate


def parse_state(field: str) -> State:
    state = collections.defaultdict(set)
    s = field.strip().splitlines()
    for i in range(5):
        for j in range(5):
            if s[i][j] == '#':
                state[0].add((i, j))
    return state


def solve(field: str, steps: int) -> int:
    state = parse_state(field)
    for _ in range(steps):
        state = simulate(state)
    return sum(len(level) for level in state.values())


def test_solve():
    assert solve("""....#
#..#.
#..##
..#..
#....""", 10) == 99


def main():
    with open('input.txt') as f:
        field = f.read().strip()
    print(solve(field, 200))


if __name__ == '__main__':
    main()
