from typing import List


def parse_image(raw_input: str, w: int, h: int) -> List[List[str]]:
    layers = []
    for offset in range(0, len(raw_input), w * h):
        layer = []
        for i in range(offset, offset + w * h, w):
            layer.append(raw_input[i:i + w])
        layers.append(layer)
    return layers


def solve(layers: List[List[str]]) -> List[str]:
    w, h = len(layers[0][0]), len(layers[0])
    composed = ['x' * w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            for layer in layers:
                if layer[i][j] != '2':
                    composed[i] = composed[i][:j] + layer[i][j] + composed[i][j+1:]
                    break
    return composed


def test_solve():
    assert solve(parse_image('0222112222120000', 2, 2)) == ['01', '10']


def main():
    layers = parse_image(input(), 25, 6)
    composed = solve(layers)
    print('\n'.join(composed).replace('0', ' ').replace('1', 'x'))


if __name__ == '__main__':
    main()
