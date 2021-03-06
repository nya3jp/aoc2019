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
Portals = Dict[Point, Tuple[Point, int]]


def find_portals(field: List[str], hole: Hole) -> Tuple[Portals, Point, Point]:
    h, w = len(field), len(field[0])
    portal_pairs = collections.defaultdict(list)

    for j in range(1, w-1):
        i = 1
        if field[i][j] in ALPHABETS:
            name = field[i-1][j] + field[i][j]
            portal_pairs[name].append(((i, j), -1))
        i = h - 2
        if field[i][j] in ALPHABETS:
            name = field[i][j] + field[i+1][j]
            portal_pairs[name].append(((i, j), -1))

    for i in range(1, h-1):
        j = 1
        if field[i][j] in ALPHABETS:
            name = field[i][j-1] + field[i][j]
            portal_pairs[name].append(((i, j), -1))
        j = w - 2
        if field[i][j] in ALPHABETS:
            name = field[i][j] + field[i][j+1]
            portal_pairs[name].append(((i, j), -1))

    for j in range(hole.sj, hole.tj):
        i = hole.si
        if field[i][j] in ALPHABETS:
            name = field[i][j] + field[i+1][j]
            portal_pairs[name].append(((i, j), 1))
        i = hole.ti - 1
        if field[i][j] in ALPHABETS:
            name = field[i-1][j] + field[i][j]
            portal_pairs[name].append(((i, j), 1))

    for i in range(hole.si, hole.ti):
        j = hole.sj
        if field[i][j] in ALPHABETS:
            name = field[i][j] + field[i][j+1]
            portal_pairs[name].append(((i, j), 1))
        j = hole.tj - 1
        if field[i][j] in ALPHABETS:
            name = field[i][j-1] + field[i][j]
            portal_pairs[name].append(((i, j), 1))

    (start, _), = portal_pairs.pop('AA')
    (goal, _), = portal_pairs.pop('ZZ')

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
        portals[pair[0][0]] = (find_adjacent(pair[1][0]), pair[0][1])
        portals[pair[1][0]] = (find_adjacent(pair[0][0]), pair[1][1])
    return portals, start, goal


Graph = Dict[Point, List[Tuple[Point, int]]]


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
                    adjs.append(((ai, aj), 0))
                elif (ai, aj) in portals:
                    adjs.append(portals[(ai, aj)])
            g[(ci, cj)] = adjs
    return g


def shortest_path(graph: Graph, start: Point, goal: Point) -> int:
    depth = 123456789
    dist = {(start, 0): 0}
    queue = collections.deque([(start, 0)])
    while queue:
        cp, cl = queue.popleft()
        if cp == goal and cl == 0:
            return dist[(cp, cl)]
        for ap, dl in graph.get(cp, []):
            al = cl + dl
            if al < 0:
                continue
            if (ap, al) in dist:
                continue
            dist[(ap, al)] = dist[(cp, cl)] + 1
            queue.append((ap, al))
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
             Z""".splitlines()) == 26
    assert solve("""             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M""".splitlines()) == 396


def main():
    with open('input.txt') as f:
        field = f.read().rstrip().splitlines()
    print(solve(field))


if __name__ == '__main__':
    main()
