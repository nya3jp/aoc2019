import itertools
from typing import List


def run(code: List[int], inputs: List[int]) -> List[int]:
    code = code[:]
    input_iter = iter(inputs)
    outputs = []
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
            code[outaddr(1)] = next(input_iter)
            pc += 2
        elif op == 4:
            outputs.append(invalue(1))
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
    return outputs


def solve(code: List[int]) -> int:
    best = 0
    for phases in itertools.permutations([0, 1, 2, 3, 4]):
        signal = 0
        for phase in phases:
            outputs = run(code, [phase, signal])
            signal = outputs[0]
        best = max(best, signal)
    return best


def test_solve():
    code = [int(s) for s in '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'.split(',')]
    assert solve(code) == 43210
    code = [int(s) for s in '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'.split(',')]
    assert solve(code) == 54321
    code = [int(s) for s in '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'.split(',')]
    assert solve(code) == 65210


def main():
    code = [int(s) for s in input().split(',')]
    print(solve(code))


if __name__ == '__main__':
    main()
