def simulate(state: int) -> int:
    newstate = 0
    for i in range(5):
        for j in range(5):
            cnt = 0
            if i > 0:
                cnt += (state >> ((i - 1) * 5 + j)) & 1
            if j > 0:
                cnt += (state >> (i * 5 + j - 1)) & 1
            if i < 4:
                cnt += (state >> ((i + 1) * 5 + j)) & 1
            if j < 4:
                cnt += (state >> (i * 5 + j + 1)) & 1
            if ((state >> (i * 5 + j)) & 1) == 0:
                if cnt == 1 or cnt == 2:
                    newstate |= 1 << (i * 5 + j)
            else:
                if cnt == 1:
                    newstate |= 1 << (i * 5 + j)
    return newstate


def test_simulate():
    assert simulate(parse_state("""....#
#..#.
#..##
..#..
#....""")) == parse_state("""#..#.
####.
###.#
##.##
.##..""")


def parse_state(field: str) -> int:
    s = ''.join(field.split())
    assert len(s) == 25
    return sum(1 << i for i, c in enumerate(s) if c == '#')


def solve(field: str) -> int:
    state = parse_state(field)
    seen = set([state])
    while True:
        state = simulate(state)
        if state in seen:
            return state
        seen.add(state)


def test_solve():
    assert solve("""....#
#..#.
#..##
..#..
#....""") == 2129920


def main():
    with open('input.txt') as f:
        field = f.read().strip()
    print(solve(field))


if __name__ == '__main__':
    main()
