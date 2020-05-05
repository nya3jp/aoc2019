import typing
from typing import Generator, Iterable, List, Union


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


def main():
    with open('input.txt') as f:
        code = [int(s) for s in f.read().strip().split(',')]

    cnt = 0
    for y in range(50):
        for x in range(50):
            output, = list(Machine(code).output([x, y]))
            print('.#'[output], end='')
            if output > 0:
                cnt += 1
        print()
    print(cnt)


if __name__ == '__main__':
    main()
