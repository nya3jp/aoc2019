import collections
import sys
import typing
from typing import Dict, List, Optional


class Component(typing.NamedTuple):
    volume: int
    chemical: str

    @staticmethod
    def parse(spec: str) -> 'Component':
        v, c = spec.strip().split()
        return Component(int(v), c)


class Reaction(typing.NamedTuple):
    sources: List[Component]
    target: Component


def parse_spec(spec: str) -> Dict[str, Reaction]:
    reactions = {}
    for line in spec.strip().splitlines():
        lhs, rhs = line.split('=>', 2)
        target = Component.parse(rhs)
        sources = [Component.parse(s) for s in lhs.split(',')]
        reactions[target.chemical] = Reaction(sources, target)
    return reactions


def pick_next(needs: Dict[str, int]) -> Optional[str]:
    for key, volume in needs.items():
        if key == 'ORE':
            continue
        if volume > 0:
            return key
    return None


def solve_unit(reactions: Dict[str, Reaction], fuel: int) -> int:
    needs = collections.defaultdict(int)
    needs.update({'FUEL': fuel})
    while True:
        next_chemical = pick_next(needs)
        if not next_chemical:
            return needs['ORE']
        reaction = reactions[next_chemical]
        target = reaction.target
        times = (needs[target.chemical] + target.volume - 1) // target.volume
        needs[target.chemical] -= target.volume * times
        for source in reaction.sources:
            needs[source.chemical] += source.volume * times


def solve(reactions: Dict[str, Reaction]) -> int:
    ore = 1000000000000
    lo, hi = 0, ore + 1
    assert solve_unit(reactions, lo) <= ore
    assert solve_unit(reactions, hi) > ore
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if solve_unit(reactions, mid) <= ore:
            lo = mid
        else:
            hi = mid
    return lo


def test_samples():
    assert solve(parse_spec("""157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""")) == 82892753
    assert solve(parse_spec("""2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF""")) == 5586022
    assert solve(parse_spec("""171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX""")) == 460664


def main():
    print(solve(parse_spec(sys.stdin.read())))


if __name__ == '__main__':
    main()
