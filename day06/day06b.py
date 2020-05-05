import sys
from typing import List, Tuple


def solve(orbits: List[Tuple[str, str]]) -> int:
    parents = {}
    for a, b in orbits:
        parents[b] = a

    def anscestors(start: str) -> List[str]:
        ans = []
        c = parents[start]
        while c:
            ans.append(c)
            c = parents.get(c)
        return ans

    you = anscestors('YOU')
    san = anscestors('SAN')

    return len(you) + len(san) - len(set(you).intersection(san)) * 2


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
K)YOU
I)SAN
"""
    orbits = [tuple(s.split(')')) for s in test_input.strip().split()]
    assert solve(orbits) == 4


def main():
    orbits = [tuple(s.split(')')) for s in sys.stdin.read().strip().split()]
    print(solve(orbits))


if __name__ == '__main__':
    main()
