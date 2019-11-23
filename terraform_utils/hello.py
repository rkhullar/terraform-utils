from pathlib import Path


def read_data() -> str:
    here: Path = Path(__file__).parent
    target = here / 'data' / 'hello.txt'
    with target.open('r') as f:
        return f.read().strip()
