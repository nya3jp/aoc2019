def solve(mini: int, maxi: int) -> int:
    cnt = 0
    for num in range(mini, maxi + 1):
        ds = str(num)
        if not ds[0] <= ds[1] <= ds[2] <= ds[3] <= ds[4] <= ds[5]:
            continue
        for i in range(6-1):
            if ds[i] == ds[i+1]:
                break
        else:
            continue
        cnt += 1
    return cnt


def test_solve():
    assert solve(111111, 111111) == 1
    assert solve(223450, 223450) == 0
    assert solve(123789, 123789) == 0


def main():
    print(solve(382345, 843167))


if __name__ == '__main__':
    main()
