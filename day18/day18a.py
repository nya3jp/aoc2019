import collections
import heapq
import itertools
from typing import Dict, List, Tuple

ALL_KEYS = 'abcdefghijklmnopqrstuvwxyz'

ADJS = (
    (-1, 0),
    (0, -1),
    (+1, 0),
    (0, +1),
)


def compute_matrix(field: List[str]) -> Dict[str, List[Tuple[int, str]]]:
    mat = {}
    h, w = len(field), len(field[0])
    for si, sj in itertools.product(range(h), range(w)):
        sc = field[si][sj]
        if sc in '#.':
            continue
        mat[sc] = []
        seen = set([(si, sj)])
        q = collections.deque([(0, si, sj)])
        while q:
            cd, ci, cj = q.popleft()
            for di, dj in ADJS:
                ni, nj = ci + di, cj + dj
                if (ni, nj) in seen:
                    continue
                seen.add((ni, nj))
                nc = field[ni][nj]
                if nc == '#':
                    continue
                nd = cd + 1
                if nc != '.':
                    mat[sc].append((nd, nc))
                    continue
                q.append((nd, ni, nj))
    return mat


def solve(field: List[str]) -> int:
    keys = ''.join(c for c in ALL_KEYS if any(c in row for row in field))
    doors = keys.upper()
    mat = compute_matrix(field)
    seen = set()
    heap = [(0, '@', '')]
    while heap:
        ct, cc, ck = heapq.heappop(heap)
        if (cc, ck) in seen:
            continue
        seen.add((cc, ck))
        if ck == keys:
            return ct
        for nd, nc in mat[cc]:
            nt, nk = ct + nd, ck
            if nc in doors and nc.lower() not in ck:
                continue
            if nc in keys and nc not in nk:
                for i, c in enumerate(nk):
                    if c > nc:
                        nk = nk[:i] + nc + nk[i:]
                        break
                else:
                    nk += nc
            if (nc, nk) in seen:
                continue
            heapq.heappush(heap, (nt, nc, nk))


def test_solve():
    assert solve("""#########
#b.A.@.a#
#########""".splitlines()) == 8
    assert solve("""########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""".splitlines()) == 86
    assert solve("""########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""".splitlines()) == 132
    assert solve("""#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""".splitlines()) == 136
    assert solve("""########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""".splitlines()) == 81


def main():
    with open('input.txt') as f:
        field = f.read().strip().splitlines()
    print(solve(field))


if __name__ == '__main__':
    main()
