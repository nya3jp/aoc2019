import sys
from typing import List


def phase(input: List[int], offset: int) -> List[int]:
    n = len(input)
    assert offset >= n // 2 + 1

    output = [0] * n
    s = 0
    for i in reversed(range(n)):
        s += input[i]
        output[i] = s % 10
    return output


def solve(input_str: str) -> str:
    input = [int(d) for d in input_str] * 10000
    offset = int(input_str[:7])
    value = input[offset:]
    for i in range(100):
        print('Phase %d' % (i + 1), file=sys.stderr)
        value = phase(value, offset)
    return ''.join(str(d) for d in value[:8])


def slow_test_solve():
    assert solve('03036732577212944063491565474664') == '84462026'
    assert solve('02935109699940807407585447034323') == '78725270'
    assert solve('03081770884921959731165446850517') == '53553731'


def main():
    print(solve(input()))


if __name__ == '__main__':
    main()
