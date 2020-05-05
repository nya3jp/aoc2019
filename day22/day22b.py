import typing


def mod(a: int, n: int) -> int:
    assert n > 0
    a -= a // n * n
    while a < 0:
        a += n
    return a


def inv(a: int, n: int) -> int:
    if a == 1:
        return 1
    return (1 - n * inv(n % a, a)) // a + n


class Operation(typing.NamedTuple):
    a: int
    b: int
    n: int

    @staticmethod
    def identity(n: int) -> 'Operation':
        return Operation(a=1, b=0, n=n)

    def apply(self, x: int) -> int:
        return mod(self.a * x + self.b, self.n)

    def compose(self, other: 'Operation') -> 'Operation':
        assert self.n == other.n
        n = self.n
        return Operation(a=mod(self.a * other.a, n), b=mod(self.b * other.a + other.b, n), n=n)

    def inverse(self) -> 'Operation':
        a = inv(self.a, self.n)
        b = mod(-self.b * a, self.n)
        return Operation(a=a, b=b, n=self.n)

    def pow(self, m: int) -> 'Operation':
        if m == 0:
            return Operation.identity(self.n)
        if m == 1:
            return self
        r = self.compose(self).pow(m // 2)
        if m % 2 == 1:
            r = r.compose(self)
        return r


def parse_operation(inst: str, n: int) -> Operation:
    if inst == 'deal into new stack':
        return Operation(a=mod(-1, n), b=mod(-1, n), n=n)  # -x-1
    if inst.startswith('cut '):
        c = int(inst.split()[-1])
        return Operation(a=1, b=mod(-c, n), n=n)  # x-c
    if inst.startswith('deal with increment '):
        f = int(inst.split()[-1])
        return Operation(a=mod(f, n), b=0, n=n)  # f*x
    assert False, 'Unknown operation: %s' % inst


def parse_operations(insts: str, n: int) -> Operation:
    op = Operation.identity(n)
    for inst in insts.strip().splitlines():
        op = op.compose(parse_operation(inst, n))
    return op


def solve(insts: str, n: int, pow: int, pos: int) -> int:
    op = parse_operations(insts, n).pow(pow)
    return op.inverse().apply(pos)


def test_solve():
    assert solve("""deal with increment 7
deal into new stack
deal into new stack""", 10, 1, 9) == 7
    assert solve("""cut 6
deal with increment 7
deal into new stack""", 10, 1, 9) == 6
    assert solve("""deal with increment 7
deal with increment 9
cut -2""", 10, 1, 9) == 9
    assert solve("""deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""", 10, 1, 9) == 6


def main():
    with open('input.txt') as f:
        insts = f.read().strip()

    print(solve(insts, n=119315717514047, pow=101741582076661, pos=2020))


if __name__ == '__main__':
    main()
