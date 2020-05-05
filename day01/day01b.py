import sys


def solve(m: int) -> int:
    f = m // 3 - 2
    if f <= 0:
        return 0
    return f + solve(f)


def test_solve():
    assert solve(14) == 2
    assert solve(1969) == 966
    assert solve(100756) == 50346


def main():
    ms = [int(s) for s in sys.stdin.read().split()]
    print(sum(solve(m) for m in ms))


if __name__ == '__main__':
    main()
