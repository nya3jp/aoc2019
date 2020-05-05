import collections
import enum
import typing
from typing import Generator, Iterable, Optional, List, Union


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


class InputInterrupt(typing.NamedTuple):
    pass


class OutputInterrupt(typing.NamedTuple):
    value: int


class Machine:
    _interpreter: Generator[Union[InputInterrupt, OutputInterrupt], int, None]

    def __init__(self, code: List[int]):
        self._interpreter = Machine._interpret(code)

    def interact(self, inputs: List[int], output_size: int) -> List[int]:
        input_pos = 0
        outputs = []
        while len(outputs) < output_size:
            interrupt = next(self._interpreter)
            if isinstance(interrupt, InputInterrupt):
                self._interpreter.send(inputs[input_pos])
                input_pos += 1
            elif isinstance(interrupt, OutputInterrupt):
                outputs.append(interrupt.value)
            else:
                raise Exception('Unknown interrupt %s' % type(interrupt))
        if input_pos < len(inputs):
            raise Exception('Excessive output')
        return outputs

    @staticmethod
    def _interpret(code: Iterable[int]) -> Generator[Union[InputInterrupt, OutputInterrupt], int, None]:
        mem = Memory(code)
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
                mem[outaddr(1)] = yield InputInterrupt()
                yield
                pc += 2
            elif op == 4:
                yield OutputInterrupt(invalue(1))
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


class Point(typing.NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)


Point.ZERO = Point(0, 0)


class Direction(enum.Enum):
    N = 1
    S = 2
    W = 3
    E = 4

    @staticmethod
    def all() -> List['Direction']:
        return [Direction.N, Direction.S, Direction.W, Direction.E]

    def flip(self) -> 'Direction':
        if self == Direction.N:
            return Direction.S
        if self == Direction.S:
            return Direction.N
        if self == Direction.W:
            return Direction.E
        if self == Direction.E:
            return Direction.W
        raise Exception('Unknown direction %s' % self)

    def delta(self) -> Point:
        if self == Direction.N:
            return Point(0, -1)
        if self == Direction.S:
            return Point(0, +1)
        if self == Direction.W:
            return Point(-1, 0)
        if self == Direction.E:
            return Point(+1, 0)
        raise Exception('Unknown direction %s' % self)


class CellType(enum.Enum):
    WALL = '#'
    FLOOR = '.'
    OXYGEN = '$'


class Cell(typing.NamedTuple):
    type: CellType
    back: Optional[Direction]


def main():
    with open('input.txt') as f:
        code = [int(s) for s in f.read().strip().split(',')]
    mac = Machine(code)

    def move(dir: Direction) -> int:
        return mac.interact([dir.value], 1)[0]

    field = {Point.ZERO: Cell(CellType.FLOOR, None)}
    queue = collections.deque()
    queue.append(Point.ZERO)
    while queue:
        next_pos = queue.popleft()
        for try_dir in Direction.all():
            try_pos = next_pos + try_dir.delta()
            if try_pos in field:
                continue
            backward_route = []
            p = next_pos
            while field[p].back:
                backward_route.append(field[p].back)
                p += field[p].back.delta()
            forward_route = []
            for dir in reversed(backward_route):
                forward_route.append(dir.flip())
            for dir in forward_route:
                assert move(dir) >= 1
            result = move(try_dir)
            field[try_pos] = Cell(
                type=(CellType.WALL, CellType.FLOOR, CellType.OXYGEN)[result],
                back=try_dir.flip())
            print(try_pos, field[try_pos])
            if result >= 1:
                queue.append(try_pos)
                assert move(try_dir.flip())
            for dir in backward_route:
                assert move(dir)
            if result == 2:
                print(len(forward_route) + 1)
                return


if __name__ == '__main__':
    main()
