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
    field = field[:]
    h, w = len(field), len(field[0])
    for i, j in itertools.product(range(h), range(w)):
        if field[i][j] == '@':
            field[i-1] = field[i-1][:j-1] + '1#2' + field[i-1][j+2:]
            field[i+0] = field[i+0][:j-1] + '###' + field[i+0][j+2:]
            field[i+1] = field[i+1][:j-1] + '3#4' + field[i+1][j+2:]
            break
    else:
        raise Exception('@ not found')

    keys = ''.join(c for c in ALL_KEYS if c in ''.join(field))
    doors = keys.upper()
    mat = compute_matrix(field)
    seen = set()
    heap = [(0, '1234', '')]
    while heap:
        ct, cv, ck = heapq.heappop(heap)
        if (cv, ck) in seen:
            continue
        seen.add((cv, ck))
        if ck == keys:
            return ct
        for ci, cc in enumerate(cv):
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
                nv = cv[:ci] + nc + cv[ci+1:]
                if (nv, nk) in seen:
                    continue
                heapq.heappush(heap, (nt, nv, nk))


def test_solve():
    assert solve("""#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######""".splitlines()) == 8
    assert solve("""###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############""".splitlines()) == 24
    assert solve("""#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############""".splitlines()) == 32
    assert solve("""#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############""".splitlines()) == 72


def main():
    with open('input.txt') as f:
        field = f.read().strip().splitlines()
    print(solve(field))


if __name__ == '__main__':
    main()
