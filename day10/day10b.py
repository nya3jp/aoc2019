import math
import sys
import typing
from typing import Dict, List


class Point(typing.NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def __floordiv__(self, value: int) -> 'Point':
        return Point(self.x // value, self.y // value)

    def norm(self) -> int:
        return self.x * self.x + self.y * self.y


def gcd(a: int, b: int) -> int:
    assert a >= 0 and b >= 0
    while b > 0:
        a, b = b, a % b
    return a


def angle(p: Point) -> float:
    # Real: (0, -1) -> (+1, 0) -> (0, +1) -> (-1, 0)
    # Conv: (-1, 0) -> (0, -1) -> (+1, 0) -> (0, +1)
    cx, cy = p.y, -p.x
    if cy == 0 and cx < 0:
        return -math.pi
    return math.atan2(cy, cx)


def test_angle():
    assert angle(Point(0, -1)) <= angle(Point(+1, 0)) <= angle(Point(0, +1)) <= angle(Point(-1, 0))


def solve(space: List[str]) -> List[Point]:
    asteroids = []
    for y, row in enumerate(space):
        for x, cell in enumerate(row):
            if cell == '#':
                asteroids.append(Point(x, y))

    def detects(center: Point) -> Dict[Point, List[Point]]:
        lines = {}
        for other in asteroids:
            if other == center:
                continue
            delta = other - center
            delta = delta // gcd(abs(delta.x), abs(delta.y))
            lines.setdefault(delta, []).append(other)
        for points in lines.values():
            points.sort(key=lambda p: (p - center).norm())
        return lines

    center = max(asteroids, key=lambda p: len(detects(p)))

    lines = detects(center)
    deltas = sorted(lines.keys(), key=angle)

    vaporized = []
    cont = True
    while cont:
        cont = False
        for delta in deltas:
            line = lines[delta]
            if line:
                vaporized.append(line[0])
                line.pop(0)
                cont = True
    return vaporized


def test_solve():
    vaporized = solve(""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""".split())
    assert vaporized[0] == Point(11, 12)
    assert vaporized[1] == Point(12, 1)
    assert vaporized[2] == Point(12, 2)
    assert vaporized[9] == Point(12, 8)
    assert vaporized[19] == Point(16, 0)
    assert vaporized[49] == Point(16, 9)
    assert vaporized[99] == Point(10, 16)
    assert vaporized[198] == Point(9, 6)
    assert vaporized[199] == Point(8, 2)
    assert vaporized[200] == Point(10, 9)
    assert vaporized[298] == Point(11, 1)


def main():
    space = sys.stdin.read().split()
    vaporized = solve(space)
    print(vaporized[200-1])


if __name__ == '__main__':
    main()
