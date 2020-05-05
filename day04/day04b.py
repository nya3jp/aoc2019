def solve(mini: int, maxi: int) -> int:
    cnt = 0
    for num in range(mini, maxi + 1):
        ds = str(num)
        if not ds[0] <= ds[1] <= ds[2] <= ds[3] <= ds[4] <= ds[5]:
            continue
        for i in range(6-1):
            if ds[i] == ds[i+1] and (i-1 < 0 or ds[i-1] != ds[i]) and (i+2 >= 6 or ds[i+1] != ds[i+2]):
                break
        else:
            continue
        cnt += 1
    return cnt


def test_solve():
    assert solve(112233, 112233) == 1
    assert solve(123444, 123444) == 0
    assert solve(111122, 111122) == 1


def main():
    print(solve(382345, 843167))


if __name__ == '__main__':
    main()
