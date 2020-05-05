import abc
import enum
import typing
from typing import Dict, Iterable, List


class Point(typing.NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)


ADJS = (
    Point(0, -1),
    Point(-1, 0),
    Point(0, +1),
    Point(+1, 0),
)


class Memory:
    _data: List[int]

    def __init__(self, data: Iterable[int]):
        self._data = list(data)

    def copy(self) -> 'Memory':
        return Memory(self._data)

    def _ensure(self, i: int) -> None:
        if i >= len(self._data):
            self._data.extend(0 for _ in range(i - len(self._data) + 1))
            assert i == len(self._data) - 1

    def __getitem__(self, i: int) -> int:
        self._ensure(i)
        return self._data[i]

    def __setitem__(self, i: int, v: int) -> None:
        self._ensure(i)
        self._data[i] = v


class IO:
    @abc.abstractmethod
    def read_input(self) -> int:
        ...

    @abc.abstractmethod
    def write_output(self, value: int) -> None:
        ...


class Machine:
    _mem: Memory
    _io: IO

    def __init__(self, mem: Memory, io: IO):
        self._mem = mem
        self._io = io

    def run(self) -> None:
        mem = self._mem
        io = self._io
        pc = 0
        rb = 0

        while True:
            op = mem[pc] % 100

            def invalue(k):
                arg = mem[pc + k]
                mode = mem[pc] // 100 // (10 ** (k - 1)) % 10
                if mode == 0:
                    return mem[arg]
                if mode == 1:
                    return arg
                if mode == 2:
                    return mem[rb + arg]
                raise Exception('Unknown arg mode %d' % mode)

            def outaddr(k):
                mode = mem[pc] // 100 // (10 ** (k - 1)) % 10
                if mode == 0:
                    return mem[pc + k]
                if mode == 1:
                    raise Exception('Immediate outaddr is invalid')
                if mode == 2:
                    return mem[pc + k] + rb
                raise Exception('Unknown arg mode %d' % mode)

            if op == 99:
                break
            elif op == 1:
                mem[outaddr(3)] = invalue(1) + invalue(2)
                pc += 4
            elif op == 2:
                mem[outaddr(3)] = invalue(1) * invalue(2)
                pc += 4
            elif op == 3:
                mem[outaddr(1)] = io.read_input()
                pc += 2
            elif op == 4:
                io.write_output(invalue(1))
                pc += 2
            elif op == 5:
                if invalue(1) != 0:
                    pc = invalue(2)
                else:
                    pc += 3
            elif op == 6:
                if invalue(1) == 0:
                    pc = invalue(2)
                else:
                    pc += 3
            elif op == 7:
                mem[outaddr(3)] = 1 if invalue(1) < invalue(2) else 0
                pc += 4
            elif op == 8:
                mem[outaddr(3)] = 1 if invalue(1) == invalue(2) else 0
                pc += 4
            elif op == 9:
                rb += invalue(1)
                pc += 2
            else:
                raise Exception('Unknown op %d' % op)


class Expect(enum.Enum):
    COLOR = 'color'
    ACTION = 'action'


def run(code: List[int]) -> Dict[Point, int]:
    mem = Memory(code)
    pos = Point(0, 0)
    dir = 0
    paint = {}

    class PainterIO(IO):
        _expect: Expect

        def __init__(self):
            self._expect = Expect.COLOR

        def read_input(self) -> int:
            return paint.get(pos, 0)

        def write_output(self, value: int) -> None:
            nonlocal pos, dir
            if self._expect == Expect.COLOR:
                assert value in (0, 1)
                paint[pos] = value
                self._expect = Expect.ACTION
            elif self._expect == Expect.ACTION:
                if value == 0:
                    dir = (dir + 1) % 4
                elif value == 1:
                    dir = (dir + 3) % 4
                else:
                    raise Exception('Invalid dir %d' % value)
                pos += ADJS[dir]
                self._expect = Expect.COLOR

    mac = Machine(mem, PainterIO())
    mac.run()
    return paint


def main():
    code = [int(s) for s in input().split(',')]
    paint = run(code)
    print(len(paint))
    w = max(p.x for p in paint.keys()) + 1
    h = max(p.y for p in paint.keys()) + 1
    for y in range(h):
        print(''.join(' #.'[paint.get(Point(x, y), 2)] for x in range(w)))


if __name__ == '__main__':
    main()
