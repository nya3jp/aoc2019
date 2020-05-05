import itertools
from typing import Generator


def factors(i: int) -> Generator[int, None, None]:
    m = i + 1
    first = True
    while True:
        yield from [0] * (m - 1 if first else m)
        yield from [1] * m
        yield from [0] * m
        yield from [-1] * m
        first = False


def phase(input_str: str) -> str:
    n = len(input_str)
    input = [int(d) for d in input_str]
    output = []
    for i in range(n):
        s = sum(d * f for d, f in zip(input, factors(i)))
        if s < 0:
            s = -s
        output.append(s % 10)
    return ''.join(str(d) for d in output)


def test_phase():
    assert phase('12345678') == '48226158'


def solve(input: str) -> str:
    value = input
    for _ in range(100):
        value = phase(value)
    return value[:8]


def test_solve():
    assert solve('80871224585914546619083218645595') == '24176176'
    assert solve('19617804207202209144916044189917') == '73745418'
    assert solve('69317163492948606335995924319873') == '52432133'


def main():
    print(solve(input()))


if __name__ == '__main__':
    main()
