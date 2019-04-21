from pathlib import Path

here = Path(__file__).parent

data = here / 'data'
target = data / 'hello.txt'


def test():
    with target.open('r') as f:
        return f.read().strip()


if __name__ == '__main__':
    print(test())
