from typing import List


Operation = List[int]


def transpose(op: Operation) -> Operation:
    tr = [-1] * len(op)
    for i, d in enumerate(op):
        tr[d] = i
    return tr


def combine(op1: Operation, op2: Operation) -> Operation:
    n = len(op1)
    return [op2[op1[i]] for i in range(n)]


def parse_operation(inst: str, n: int) -> Operation:
    if inst == 'deal into new stack':
        rop = list(reversed(range(n)))
        return transpose(rop)
    if inst.startswith('cut '):
        pos = int(inst.split()[-1])
        if pos < 0:
            pos = n + pos
        rop = list(range(pos, n)) + list(range(0, pos))
        return transpose(rop)
    if inst.startswith('deal with increment '):
        f = int(inst.split()[-1])
        rop = [-1] * n
        for i in range(n):
            rop[i * f % n] = i
        return transpose(rop)
    assert False, 'Unknown operation: %s' % inst


def parse_operations(insts: str, n: int) -> List[Operation]:
    return [parse_operation(line, n) for line in insts.strip().splitlines()]


def solve(insts: str, n: int) -> List[int]:
    ops = parse_operations(insts, n)
    cop = list(range(n))
    for op in ops:
        cop = combine(cop, op)
    return transpose(cop)


def test_solve():
    assert solve("""deal with increment 7
deal into new stack
deal into new stack""", 10) == [int(s) for s in '0 3 6 9 2 5 8 1 4 7'.split()]
    assert solve("""cut 6
deal with increment 7
deal into new stack""", 10) == [int(s) for s in '3 0 7 4 1 8 5 2 9 6'.split()]
    assert solve("""deal with increment 7
deal with increment 9
cut -2""", 10) == [int(s) for s in '6 3 0 7 4 1 8 5 2 9'.split()]
    assert solve("""deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""", 10) == [int(s) for s in '9 2 5 8 1 4 7 0 3 6'.split()]


def main():
    with open('input.txt') as f:
        insts = f.read().strip()
    deck = solve(insts, 10007)
    print(deck.index(2019))


if __name__ == '__main__':
    main()
