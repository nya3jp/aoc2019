from typing import List


def parse_image(raw_input: str) -> List[str]:
    w, h = 25, 6
    n = len(raw_input) // (w * h)
    layers = []
    for i in range(0, len(raw_input), w * h):
        j = i + w * h
        layers.append(raw_input[i:j])
    return layers


def solve(layers: List[str]):
    layer = min(layers, key=lambda l: sum(1 for px in l if px == '0'))
    return sum(1 for px in layer if px == '1') * sum(1 for px in layer if px == '2')


def main():
    layers = parse_image(input())
    print(solve(layers))


if __name__ == '__main__':
    main()
