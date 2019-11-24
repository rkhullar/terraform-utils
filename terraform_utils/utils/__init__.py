from typing import Dict, Iterator, List, NamedTuple, Optional, Pattern, Union
from pathlib import Path
import re

from .mockio import mock_input_output

__all__ = ['read_hello_txt', 'Variable', 'find_target', 'parse_config', 'load_config',
           'build_default_common_values', 'write_common_values', 'mock_input_output']


def read_hello_txt() -> str:
    here: Path = Path(__file__).parents[1]
    target = here / 'data' / 'hello.txt'
    with target.open('r') as f:
        return f.read().strip()


class Variable(NamedTuple):
    key: str
    val: str

    @staticmethod
    def build_pattern() -> Pattern:
        return re.compile(r'^\s*"?(?P<key>[-.\w]+)"?\s*=\s*"?(?P<val>[-.\w@]+)"?\s*(\Z|#.*)$')

    @classmethod
    def from_dict(cls, data) -> List['Variable']:
        return [Variable(key, val) for key, val in data.items()]


def find_target(name: str, start_dir: Path = None, root_dir: Path = None) -> Optional[Path]:
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


def build_default_common_values() -> Dict[str, str]:
    return dict(app_name='example', region='us-east-1', company='company', owner='noreply@example.com')


def write_common_values(target: Union[Path, str], common_values: Dict[str, str] = None):
    common_values = common_values or build_default_common_values()
    with Path(target).open('w') as f:
        for key, val in common_values.items():
            print(f'{key} = {val}', file=f)
