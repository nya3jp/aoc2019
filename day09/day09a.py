import abc
from typing import Iterable, Iterator, List


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


class StaticIO(IO):
    _input_iter: Iterator[int]
    outputs: List[int]

    def __init__(self, inputs: Iterable[int]):
        self._input_iter = iter(inputs)
        self.outputs = []

    def read_input(self) -> int:
        return next(self._input_iter)

    def write_output(self, value: int) -> None:
        self.outputs.append(value)


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


def run(code: List[int], inputs: List[int]) -> List[int]:
    mem = Memory(code)
    io = StaticIO(inputs)
    mac = Machine(mem, io)
    mac.run()
    return io.outputs


def test_run():
    code = [int(s) for s in '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'.split(',')]
    assert run(code, []) == code


def main():
    code = [int(s) for s in input().split(',')]
    print(run(code, [1]))


if __name__ == '__main__':
    main()
