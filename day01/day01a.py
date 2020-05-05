import sys


def solve(m: int) -> int:
    return m // 3 - 2


def test_solve():
    assert solve(12) == 2
    assert solve(14) == 2
    assert solve(1969) == 654
    assert solve(100756) == 33583


def main():
    ms = [int(s) for s in sys.stdin.read().split()]
    print(sum(solve(m) for m in ms))


if __name__ == '__main__':
    main()
