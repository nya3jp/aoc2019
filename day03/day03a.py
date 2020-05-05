import typing
from typing import List, Set


class Point(typing.NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)


class Segment(typing.NamedTuple):
    dir: Point
    len: int

    _DIRS = {
        'R': Point(1, 0),
        'L': Point(-1, 0),
        'U': Point(0, 1),
        'D': Point(0, -1),
    }

    @staticmethod
    def parse(s: str) -> 'Segment':
        return Segment(Segment._DIRS[s[0]], int(s[1:]))


def trace(wire: List[Segment]) -> Set[Point]:
    ps = set()
    p = Point(0, 0)
    for seg in wire:
        for _ in range(seg.len):
            p += seg.dir
            ps.add(p)
    return ps


def solve(wire1: List[Segment], wire2: List[Segment]) -> int:
    trace1 = trace(wire1)
    trace2 = trace(wire2)
    intersects = trace1.intersection(trace2)
    return min(abs(p.x) + abs(p.y) for p in intersects)


def parse_wire(s: str) -> List[Segment]:
    return [Segment.parse(seg) for seg in s.split(',')]


def test_solve():
    assert solve(parse_wire('R75,D30,R83,U83,L12,D49,R71,U7,L72'), parse_wire('U62,R66,U55,R34,D71,R55,D58,R83')) == 159
    assert solve(parse_wire('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'), parse_wire('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7')) == 135


def main():
    wire1 = parse_wire(input())
    wire2 = parse_wire(input())
    print(solve(wire1, wire2))


if __name__ == '__main__':
    main()
