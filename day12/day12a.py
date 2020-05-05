import dataclasses
import typing
from typing import List


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
        def sign(i: int):
            if i == 0:
                return 0
            if i > 0:
                return 1
            return -1
        return Point(sign(self.x), sign(self.y), sign(self.z))


@dataclasses.dataclass
class Moon:
    position: Point
    velocity: Point

    @staticmethod
    def static(x: int, y: int, z: int) -> 'Moon':
        return Moon(Point(x, y, z), Point(0, 0, 0))

    def energy(self) -> int:
        return self.position.abs() * self.velocity.abs()


def simulate(moons: List[Moon]) -> None:
    for i, moon in enumerate(moons):
        for j, other in enumerate(moons):
            if i == j:
                continue
            moon.velocity += (other.position - moon.position).unit()
    for moon in moons:
        moon.position += moon.velocity


def energy(moons: List[Moon]) -> int:
    return sum(moon.energy() for moon in moons)


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
    for _ in range(10):
        simulate(moons)
    # After 10 steps:
    # pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
    # pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
    # pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
    # pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>
    assert moons == [
        Moon(Point(2, 1, -3), Point(-3, -2, 1)),
        Moon(Point(1, -8, 0), Point(-1, 1, 3)),
        Moon(Point(3, -6, 1), Point(3, 2, -3)),
        Moon(Point(2, 0, 4), Point(1, -1, -1)),
    ]
    # Energy after 10 steps:
    # pot: 2 + 1 + 3 =  6;   kin: 3 + 2 + 1 = 6;   total:  6 * 6 = 36
    # pot: 1 + 8 + 0 =  9;   kin: 1 + 1 + 3 = 5;   total:  9 * 5 = 45
    # pot: 3 + 6 + 1 = 10;   kin: 3 + 2 + 3 = 8;   total: 10 * 8 = 80
    # pot: 2 + 0 + 4 =  6;   kin: 1 + 1 + 1 = 3;   total:  6 * 3 = 18
    assert energy(moons) == 179


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
    for _ in range(1000):
        simulate(moons)
    print(energy(moons))


if __name__ == '__main__':
    main()
