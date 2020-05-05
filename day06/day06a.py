import sys
from typing import List, Tuple


def solve(orbits: List[Tuple[str, str]]) -> int:
    parents = {}
    for a, b in orbits:
        parents[b] = a
    cnt = 0
    for _, c in orbits:
        while True:
            p = parents.get(c)
            if p is None:
                break
            c = p
            cnt += 1
    return cnt


def test_solve():
    test_input = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""
    orbits = [tuple(s.split(')')) for s in test_input.strip().split()]
    assert solve(orbits) == 42


def main():
    orbits = [tuple(s.split(')')) for s in sys.stdin.read().strip().split()]
    print(solve(orbits))


if __name__ == '__main__':
    main()
