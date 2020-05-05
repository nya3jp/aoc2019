import collections
import random
import re
import sys
import typing
from typing import Dict, Generator, Iterable, List, Optional, Tuple, Union


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


class Room(typing.NamedTuple):
    name: str
    desc: str
    doors: List[str]
    items: List[str]


_ROOM_RE = re.compile(r"""== (?P<name>.*) ==
(?P<desc>.*)

Doors here lead:
(?P<doors>(- .*
)+)
(Items here:
(?P<items>(- .*
)+)
)?""")

GOOD_ITEMS = (
    'dehydrated water',
    'ornament',
    'sand',
    'astrolabe',
    'shell',
    'klein bottle',
    'semiconductor',
    'mutex',
)
BAD_ITEMS = (
    'photons',
    'escape pod',
    'infinite loop',
    'giant electromagnet',
    'molten lava',
)


def opposite(dir: str) -> str:
    return {
        'north': 'south',
        'south': 'north',
        'west': 'east',
        'east': 'west',
    }[dir]


class Droid:
    _code: List[int]
    _mac: Machine
    _rooms: Dict[str, Room]
    _mapping: Dict[Tuple[str, str], str]

    def __init__(self, code: List[int]):
        self._code = code
        self._mac = Machine(code)
        self._rooms = {}
        self._mapping = {}

    def restart(self) -> 'Droid':
        copy = Droid(self._code)
        copy._rooms = self._rooms
        copy._mapping = self._mapping
        return copy

    def init_explore(self) -> None:
        room, = Droid._parse_rooms(self._command(''))
        self._rooms[room.name] = room
        current_name = room.name

        while True:
            try:
                next_name, next_dir = self._find_unexplored()
            except StopIteration:
                break
            #print('# Next: %s %s' % (next_name, next_dir))
            route = self._find_route(current_name, next_name)
            for dir in route:
                self._command(dir)
            rooms = Droid._parse_rooms(self._command(next_dir))
            self._rooms.setdefault(rooms[0].name, rooms[0])
            #print('# Learn: %s -- %s --> %s' % (next_name, next_dir, rooms[0].name))
            self._mapping[(next_name, next_dir)] = rooms[0].name
            #print('# Learn: %s -- %s --> %s' % (rooms[0].name, opposite(next_dir), next_name))
            self._mapping[(rooms[0].name, opposite(next_dir))] = next_name
            current_name = rooms[-1].name

        print(self._mapping)

    def take_and_try(self, takes: List[str]) -> None:
        room, = Droid._parse_rooms(self._command(''))
        current_name = room.name

        for item in takes:
            for room in self._rooms.values():
                if item in room.items:
                    break
            else:
                assert False, '%s not found' % item
            route = self._find_route(current_name, room.name)
            for dir in route:
                self._command(dir)
            current_name = room.name
            text = self._command('take %s' % item)
            assert 'You take' in text, text

        route = self._find_route(current_name, 'Security Checkpoint')
        for dir in route:
            self._command(dir)
        text = self._command('south')
        if 'you are ejected' in text:
            return
        print(text)
        sys.exit(0)

    def _find_unexplored(self) -> Tuple[str, str]:
        for room in self._rooms.values():
            for dir in room.doors:
                if (room.name, dir) not in self._mapping:
                    return room.name, dir
        raise StopIteration()

    def _find_route(self, src: str, dst: str) -> List[str]:
        reverse_trace: Dict[str, Tuple[str, str]] = {src: None}
        queue = collections.deque([src])
        while queue:
            cur = queue.popleft()
            if cur == dst:
                break
            for dir in self._rooms[cur].doors:
                next = self._mapping.get((cur, dir))
                if next and next not in reverse_trace:
                    reverse_trace[next] = (cur, dir)
                    queue.append(next)
        else:
            assert False, 'No route'
        reverse_route = []
        cur = dst
        while reverse_trace[cur]:
            prev, dir = reverse_trace[cur]
            reverse_route.append(dir)
            cur = prev
        return list(reversed(reverse_route))

    def _command(self, cmd: str) -> str:
        inputs = [ord(c) for c in (cmd + '\n\n')]
        input_pos = 0
        outputs = []
        while input_pos < len(inputs):
            intr = self._mac.wait_interrupt(inputs[input_pos])
            if intr is None:
                break
            if isinstance(intr, InputInterrupt):
                input_pos += 1
            elif isinstance(intr, OutputInterrupt):
                outputs.append(intr.value)
            else:
                assert False, intr
        text = ''.join(chr(c) for c in outputs)
        #sys.stdout.write(text)
        return text

    @staticmethod
    def _parse_rooms(text: str) -> List[Room]:
        rooms = []
        for m in _ROOM_RE.finditer(text):
            doors = (m.group('doors') or '').replace('- ', '').strip().splitlines()
            items = (m.group('items') or '').replace('- ', '').strip().splitlines()
            rooms.append(Room(
                name=m.group('name'),
                desc=m.group('desc'),
                doors=doors,
                items=items))
        return rooms


def test_parse():
    assert Droid._parse_rooms("""== Hull Breach ==
You got in through a hole in the floor here. To keep your ship from also freezing, the hole has been sealed.

Doors here lead:
- north
- east
- west

Command?
""")


T = typing.TypeVar('T')


def combination(v: List[T]) -> Iterable[List[T]]:
    if not v:
        yield []
        return
    for u in combination(v[:-1]):
        yield u
        yield u + [v[-1]]


def main():
    with open('input.txt') as f:
        code = [int(s) for s in f.read().strip().split(',')]

    droid = Droid(code)
    droid.init_explore()

    for takes in combination(GOOD_ITEMS):
        print('Trying %s' % ', '.join(takes))
        droid = droid.restart()
        droid.take_and_try(takes)


if __name__ == '__main__':
    main()
