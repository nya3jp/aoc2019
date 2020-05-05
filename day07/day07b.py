import itertools
from typing import Generator, List


def run(code: List[int]) -> Generator[int, int, None]:
    code = code[:]
    output = None
    pc = 0
    while True:
        op = code[pc] % 100

        def invalue(k):
            arg = code[pc + k]
            mode = code[pc] // 100 // (10 ** (k - 1)) % 10
            if mode == 0:
                return code[arg]
            if mode == 1:
                return arg
            raise Exception('Unknown arg mode %d' % mode)

        def outaddr(k):
            return code[pc + k]

        if op == 99:
            break
        elif op == 1:
            code[outaddr(3)] = invalue(1) + invalue(2)
            pc += 4
        elif op == 2:
            code[outaddr(3)] = invalue(1) * invalue(2)
            pc += 4
        elif op == 3:
            code[outaddr(1)] = yield output
            output = None
            pc += 2
        elif op == 4:
            assert output is None
            output = invalue(1)
            pc += 2
        elif op == 5:
            if invalue(1) != 0:
                pc = invalue(2)
            else:
                pc += 3
        elif op == 6:
            if invalue(1) == 0:
                pc = invalue(2)
            else:
                pc += 3
        elif op == 7:
            code[outaddr(3)] = 1 if invalue(1) < invalue(2) else 0
            pc += 4
        elif op == 8:
            code[outaddr(3)] = 1 if invalue(1) == invalue(2) else 0
            pc += 4
        else:
            raise Exception('Unknown op %d' % op)
    assert output is not None
    yield output


def solve(code: List[int]) -> int:
    best = 0
    for phases in itertools.permutations([5, 6, 7, 8, 9]):
        signal = 0
        machines = []
        for phase in phases:
            m = run(code)
            m.send(None)
            m.send(phase)
            machines.append(m)
        try:
            while True:
                for m in machines:
                    signal = m.send(signal)
        except StopIteration:
            pass
        best = max(best, signal)
    return best


def test_solve():
    code = [int(s) for s in '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'.split(',')]
    assert solve(code) == 139629729
    code = [int(s) for s in '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'.split(',')]
    assert solve(code) == 18216


def main():
    code = [int(s) for s in input().split(',')]
    print(solve(code))


if __name__ == '__main__':
    main()
