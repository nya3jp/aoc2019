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
        else:
            raise Exception('Unknown op %d' % op)
    return outputs


def main():
    code = [int(s) for s in input().split(',')]
    inputs = [1]
    outputs = run(code, inputs)
    print(','.join(str(k) for k in outputs))


if __name__ == '__main__':
    main()
