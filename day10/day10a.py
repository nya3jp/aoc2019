import sys
import typing
from typing import List


class Point(typing.NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def __floordiv__(self, value: int) -> 'Point':
        return Point(self.x // value, self.y // value)


def gcd(a: int, b: int) -> int:
    assert a >= 0 and b >= 0
    while b > 0:
        a, b = b, a % b
    return a


def solve(space: List[str]) -> int:
    asteroids = []
    for y, row in enumerate(space):
        for x, cell in enumerate(row):
            if cell == '#':
                asteroids.append(Point(x, y))

    best = 0
    for center in asteroids:
        angles = set()
        for other in asteroids:
            if other == center:
                continue
            delta = other - center
            angle = delta // gcd(abs(delta.x), abs(delta.y))
            angles.add(angle)
        best = max(best, len(angles))

    return best


def test_solve():
    assert solve("""......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""".split()) == 33
    assert solve("""#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""".split()) == 35
    assert solve(""".#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""".split()) == 41
    assert solve(""".#..##.###...#######
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
###.##.####.##.#..##""".split()) == 210


def main():
    space = sys.stdin.read().split()
    print(solve(space))


if __name__ == '__main__':
    main()
