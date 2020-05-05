import dataclasses
import enum
import typing
from typing import List, Tuple


def sign(i: int):
    if i == 0:
        return 0
    if i > 0:
        return 1
    return -1


class Axis(enum.Enum):
    X = 'x'
    Y = 'y'
    Z = 'z'


class Point(typing.NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def abs(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def unit(self) -> 'Point':
        return Point(sign(self.x), sign(self.y), sign(self.z))

    def axis(self, a: Axis) -> int:
        if a == Axis.X:
            return self.x
        if a == Axis.Y:
            return self.y
        if a == Axis.Z:
            return self.z
        raise ValueError('Unknown axis %s' % a)


@dataclasses.dataclass
class Moon:
    position: Point
    velocity: Point

    @staticmethod
    def static(x: int, y: int, z: int) -> 'Moon':
        return Moon(Point(x, y, z), Point(0, 0, 0))

    def energy(self) -> int:
        return self.position.abs() * self.velocity.abs()


def gcd(a: int, b: int) -> int:
    assert a >= 0 and b >= 0
    while b > 0:
        a, b = b, a % b
    return a


class Pattern(typing.NamedTuple):
    start: int
    period: int

    def intersection(self, other: 'Pattern') -> 'Pattern':
        assert self.start == 0 and other.start == 0  # unproved
        return Pattern(0, self.period * other.period // gcd(self.period, other.period))


class Object(typing.NamedTuple):
    position: int
    velocity: int


def find_pattern_axis(moons: List[Moon], axis: Axis) -> Pattern:
    n = len(moons)
    state = tuple(Object(moon.position.axis(axis), moon.velocity.axis(axis)) for moon in moons)
    seen = {}
    step = 0
    while True:
        if state in seen:
            return Pattern(seen[state], step - seen[state])
        seen[state] = step
        step += 1
        gravity = [0] * n
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                gravity[i] += sign(state[j].position - state[i].position)
        state = tuple(
            Object(obj.position + obj.velocity + g, obj.velocity + g)
            for obj, g in zip(state, gravity))


def find_pattern(moons: List[Moon]) -> Pattern:
    p = Pattern(0, 1)
    for a in (Axis.X, Axis.Y, Axis.Z):
        p = p.intersection(find_pattern_axis(moons, a))
    return p


def test_sample():
    # <x=-1, y=0, z=2>
    # <x=2, y=-10, z=-7>
    # <x=4, y=-8, z=8>
    # <x=3, y=5, z=-1>
    moons = [
        Moon.static(-1, 0, 2),
        Moon.static(2, -10, -7),
        Moon.static(4, -8, 8),
        Moon.static(3, 5, -1),
    ]
    assert find_pattern(moons) == Pattern(0, 2772)


def main():
    # <x=-7, y=-8, z=9>
    # <x=-12, y=-3, z=-4>
    # <x=6, y=-17, z=-9>
    # <x=4, y=-10, z=-6>
    moons = [
        Moon.static(-7, -8, 9),
        Moon.static(-12, -3, -4),
        Moon.static(6, -17, -9),
        Moon.static(4, -10, -6),
    ]
    print(find_pattern(moons))


if __name__ == '__main__':
    main()
