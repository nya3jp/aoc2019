import itertools
import sys
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

    def output(self, inputs: List[int]) -> Generator[int, None, None]:
        input_pos = 0
        while True:
            try:
                interrupt = next(self._interpreter)
            except StopIteration:
                break
            if isinstance(interrupt, InputInterrupt):
                self._interpreter.send(inputs[input_pos])
                input_pos += 1
            elif isinstance(interrupt, OutputInterrupt):
                yield interrupt.value
            else:
                raise Exception('Unknown interrupt %s' % type(interrupt))
        if input_pos < len(inputs):
            raise Exception('Excessive output')

    def interact(self, inputs: List[int], output_size: Optional[int]) -> List[int]:
        input_pos = 0
        outputs = []
        while output_size is None or len(outputs) < output_size:
            try:
                interrupt = next(self._interpreter)
            except StopIteration:
                break
            if isinstance(interrupt, InputInterrupt):
                self._interpreter.send(inputs[input_pos])
                input_pos += 1
            elif isinstance(interrupt, OutputInterrupt):
                outputs.append(interrupt.value)
            else:
                raise Exception('Unknown interrupt %s' % type(interrupt))
        if input_pos < len(inputs):
            raise Exception('Excessive output')
        if output_size is not None and len(outputs) < output_size:
            raise Exception('Insufficient output')
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


_ADJ = (
    (-1, 0),
    (0, -1),
    (+1, 0),
    (0, +1),
)


def find_route(code: List[int]) -> int:
    mac = Machine(code)
    outputs = mac.interact([], None)
    field = [list(line) for line in ''.join(chr(i) for i in outputs).strip().splitlines()]

    # Padding
    field.insert(0, ['.'] * len(field[0]))
    field.append(['.'] * len(field[0]))
    for i in range(len(field)):
        field[i] = ['.'] + field[i] + ['.']
    h, w = len(field), len(field[0])

    cdir = 0
    for ci, cj in itertools.product(range(h), range(w)):
        if field[ci][cj] == '^':
            break

    while True:
        for turn in (1, 3):
            ndir = (cdir + turn) % 4
            di, dj =_ADJ[ndir][0], _ADJ[ndir][1]
            ni, nj = ci + di, cj + dj
            if field[ni][nj] != '.':
                break
        else:
            break
        l = 1
        while field[ci + di * (l + 1)][cj + dj * (l + 1)] != '.':
            l += 1
        print('%s,%d' % ('L' if turn == 1 else 'R', l))
        ci += di * l
        cj += dj * l
        cdir = ndir


_SOLUTION = """A,C,A,B,C,B,C,B,A,B
R,12,L,6,R,12
R,12,L,10,L,6,R,10
L,8,L,6,L,10
n
"""


def main():
    with open('input.txt') as f:
        code = [int(s) for s in f.read().strip().split(',')]

    # find_route(code)

    code[0] = 2
    mac = Machine(code)
    for c in mac.output([ord(c) for c in _SOLUTION]):
        if c >= 256:
            print(c)
        else:
            sys.stdout.write(chr(c))


if __name__ == '__main__':
    main()
