from typing import Dict, Iterator, NamedTuple, Pattern
from pathlib import Path
import re

__all__ = ['read_hello_txt', 'Variable', 'find_target', 'parse_config', 'load_config']


def read_hello_txt() -> str:
    here: Path = Path(__file__).parent
    target = here / 'data' / 'hello.txt'
    with target.open('r') as f:
        return f.read().strip()


class Variable(NamedTuple):
    key: str
    val: str

    @staticmethod
    def build_pattern() -> Pattern:
        return re.compile(r'^\s*"?(?P<key>[-.\w]+)"?\s*=\s*"?(?P<val>[-.\w@]+)"?\s*(\Z|#.*)$')


def find_target(name: str, start_dir: Path = None, root_dir: Path = None) -> Path:
    work_dir = start_dir or Path().absolute()
    root_dir = root_dir or Path(work_dir.root)
    while work_dir != root_dir:
        potential = work_dir / name
        if potential.exists():
            return potential
        work_dir = work_dir.parent


def parse_config(path: Path) -> Iterator[Variable]:
    pattern = Variable.build_pattern()
    with path.open('r') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                yield Variable(**match.groupdict())


def load_config(path: Path) -> Dict[str, str]:
    return {var.key: var.val for var in parse_config(path)}
