import collections
import typing
from typing import Dict, List, Tuple


ALPHABETS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ADJS = (
    (-1, 0),
    (0, -1),
    (+1, 0),
    (0, +1),
)


class Hole(typing.NamedTuple):
    si: int
    sj: int
    ti: int
    tj: int


def normalize_field(field: List[str]) -> List[str]:
    w = max(len(row.rstrip()) for row in field)
    for i, row in enumerate(field):
        row = row.rstrip()
        field[i] = row + ' ' * (w - len(row))
        assert len(field[i]) == w
    return field


def find_hole(field: List[str]) -> Hole:
    h, w = len(field), len(field[0])
    for si, row in enumerate(field):
        if si < 2 or si >= h-2:
            continue
        for sj, c in enumerate(row):
            if sj < 2 or sj >= w-2:
                continue
            if c != ' ':
                continue
            ti = si + 1
            while field[ti][sj] not in '#.':
                ti += 1
            tj = sj + 1
            while field[si][tj] not in '#.':
                tj += 1
            return Hole(si, sj, ti, tj)
    raise Exception('Hole not found')


Point = Tuple[int, int]
Portals = Dict[Point, Point]


def find_portals(field: List[str], hole: Hole) -> Tuple[Portals, Point, Point]:
    h, w = len(field), len(field[0])
    portal_pairs = collections.defaultdict(list)

    for j in range(1, w-1):
        i = 1
        if field[i][j] in ALPHABETS:
            name = field[i-1][j] + field[i][j]
            portal_pairs[name].append((i, j))
        i = h - 2
        if field[i][j] in ALPHABETS:
            name = field[i][j] + field[i+1][j]
            portal_pairs[name].append((i, j))

    for i in range(1, h-1):
        j = 1
        if field[i][j] in ALPHABETS:
            name = field[i][j-1] + field[i][j]
            portal_pairs[name].append((i, j))
        j = w - 2
        if field[i][j] in ALPHABETS:
            name = field[i][j] + field[i][j+1]
            portal_pairs[name].append((i, j))

    for j in range(hole.sj, hole.tj):
        i = hole.si
        if field[i][j] in ALPHABETS:
            name = field[i][j] + field[i+1][j]
            portal_pairs[name].append((i, j))
        i = hole.ti - 1
        if field[i][j] in ALPHABETS:
            name = field[i-1][j] + field[i][j]
            portal_pairs[name].append((i, j))

    for i in range(hole.si, hole.ti):
        j = hole.sj
        if field[i][j] in ALPHABETS:
            name = field[i][j] + field[i][j+1]
            portal_pairs[name].append((i, j))
        j = hole.tj - 1
        if field[i][j] in ALPHABETS:
            name = field[i][j-1] + field[i][j]
            portal_pairs[name].append((i, j))

    start, = portal_pairs.pop('AA')
    goal, = portal_pairs.pop('ZZ')

    def find_adjacent(p: Point) -> Point:
        for di, dj in ADJS:
            ai, aj = p[0] + di, p[1] + dj
            if field[ai][aj] == '.':
                return ai, aj
        assert False, 'No adjacent floor'

    start = find_adjacent(start)
    goal = find_adjacent(goal)

    portals = {}
    for name, pair in portal_pairs.items():
        assert len(pair) == 2, (name, pair)
        portals[pair[0]] = find_adjacent(pair[1])
        portals[pair[1]] = find_adjacent(pair[0])
    return portals, start, goal


Graph = Dict[Point, List[Point]]


def build_graph(field: List[str], portals: Portals) -> Graph:
    g = {}
    for ci, row in enumerate(field):
        for cj, c in enumerate(row):
            if c != '.':
                continue
            adjs = []
            for di, dj in ADJS:
                ai, aj = ci + di, cj + dj
                if field[ai][aj] == '.':
                    adjs.append((ai, aj))
                elif (ai, aj) in portals:
                    adjs.append(portals[(ai, aj)])
            g[(ci, cj)] = adjs
    return g


def shortest_path(graph: Graph, start: Point, goal: Point) -> int:
    dist = {start: 0}
    queue = collections.deque([start])
    while queue:
        cp = queue.popleft()
        if cp == goal:
            return dist[goal]
        for ap in graph.get(cp, []):
            if ap in dist:
                continue
            dist[ap] = dist[cp] + 1
            queue.append(ap)
    assert False, 'No route'


def solve(field: List[str]) -> int:
    field = normalize_field(field)
    hole = find_hole(field)
    portals, start, goal = find_portals(field, hole)
    graph = build_graph(field, portals)
    return shortest_path(graph, start, goal)


def test_solve():
    assert solve("""         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z""".splitlines()) == 23
    assert solve("""                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P   """.splitlines()) == 58


def main():
    with open('input.txt') as f:
        field = f.read().rstrip().splitlines()
    print(solve(field))


if __name__ == '__main__':
    main()
