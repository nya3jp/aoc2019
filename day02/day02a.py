from typing import List


def run(code: List[int]) -> List[int]:
    code = code[:]
    pc = 0
    while True:
        op = code[pc]
        if op == 99:
            break
        elif op == 1:
            a, b, c = code[pc + 1:pc + 4]
            code[c] = code[a] + code[b]
            pc += 4
        elif op == 2:
            a, b, c = code[pc + 1:pc + 4]
            code[c] = code[a] * code[b]
            pc += 4
        else:
            raise Exception('Unknown op %d' % op)
    return code


def test_run():
    assert run([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]) == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    assert run([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
    assert run([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
    assert run([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
    assert run([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]


def main():
    code = [int(s) for s in input().split(',')]
    code[1] = 12
    code[2] = 2
    print(run(code)[0])


if __name__ == '__main__':
    main()
