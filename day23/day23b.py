import collections
import typing
from typing import Generator, Iterable, List, Optional, Union


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


Interrupt = Union[InputInterrupt, OutputInterrupt]


class Machine:
    _interpreter: Generator[Union[InputInterrupt, OutputInterrupt], int, None]

    def __init__(self, code: List[int]):
        self._interpreter = Machine._interpret(code)

    def communicate(self, inputs: Iterable[int]) -> Iterable[int]:
        input_iter = iter(inputs)
        while True:
            try:
                interrupt = next(self._interpreter)
            except StopIteration:
                break
            if isinstance(interrupt, InputInterrupt):
                self._interpreter.send(next(input_iter))
            elif isinstance(interrupt, OutputInterrupt):
                yield interrupt.value
            else:
                raise Exception('Unknown interrupt %s' % type(interrupt))

    def send(self, inputs: List[int]) -> None:
        input_pos = 0
        while input_pos < len(inputs):
            try:
                interrupt = next(self._interpreter)
            except StopIteration:
                raise Exception('Unexpected halt')
            if isinstance(interrupt, InputInterrupt):
                self._interpreter.send(inputs[input_pos])
                input_pos += 1
            elif isinstance(interrupt, OutputInterrupt):
                raise Exception('Unexpected output')
            else:
                raise Exception('Unknown interrupt %s' % type(interrupt))

    def receive(self, size: int) -> List[int]:
        outputs = []
        while len(outputs) < size:
            try:
                interrupt = next(self._interpreter)
            except StopIteration:
                raise Exception('Unexpected halt')
            if isinstance(interrupt, InputInterrupt):
                raise Exception('Unexpected input')
            elif isinstance(interrupt, OutputInterrupt):
                outputs.append(interrupt.value)
            else:
                raise Exception('Unknown interrupt %s' % type(interrupt))
        return outputs

    def wait_interrupt(self, next_input: int) -> Optional[Interrupt]:
        try:
            interrupt = next(self._interpreter)
        except StopIteration:
            return None
        if isinstance(interrupt, InputInterrupt):
            self._interpreter.send(next_input)
        return interrupt

    @staticmethod
    def _interpret(code: Iterable[int]) -> Generator[Interrupt, int, None]:
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

    n = 50

    macs = [Machine(code) for _ in range(n)]
    for i, mac in enumerate(macs):
        mac.send([i])

    queues = [collections.deque() for _ in macs]
    cur_nat = None
    last_nat = None
    idle = 0
    while True:
        active = False
        for i, mac in enumerate(macs):
            q = queues[i]
            intr = mac.wait_interrupt(q[0] if q else -1)
            assert intr is not None, 'Machine %d halted' % i
            if isinstance(intr, InputInterrupt):
                if q:
                    q.popleft()
                    active = True
            if isinstance(intr, OutputInterrupt):
                active = True
                dest = intr.value
                x, y = mac.receive(2)
                if dest == 255:
                    print('NAT set: (%d, %d)' % (x, y))
                    cur_nat = (x, y)
                else:
                    queues[dest].extend([x, y])
        if not active:
            idle += 1
            if idle >= 3:
                print('NAT send: (%d, %d)' % (cur_nat[0], cur_nat[1]))
                if last_nat and cur_nat[1] == last_nat[1]:
                    print(cur_nat[1])
                    return
                queues[0].extend(cur_nat)
                last_nat = cur_nat


if __name__ == '__main__':
    main()
