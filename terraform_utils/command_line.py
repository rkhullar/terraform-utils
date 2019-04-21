from typing import Dict, Iterator, NamedTuple, Pattern
from argparse import ArgumentParser
from pathlib import Path
import re


def build_parser():
    parser = ArgumentParser()
    parser.add_argument('-t', '--target', type=str, default='common', help='tfvars search target')
    parser.add_argument('-k', '--key', type=str, help='variable to read')
    parser.add_argument('-c', '--component', choices=['bucket', 'object', 'table', 'env'])
    parser.add_argument('-x', '--extension', type=str, default='tfvars')
    parser.add_argument('--bucket-name', type=str, default='terraformstate')
    parser.add_argument('--table-name', type=str, default='terraformlock')
    parser.add_argument('--prefix', type=str, default='${app_name}-')
    parser.add_argument('--suffix', type=str, default='-${env}-${company}')
    parser.add_argument('--state-name', type=str, default='terraform.tfstate')
    return parser


def find_target(name: str, start_dir: Path = None, root_dir: Path = None) -> Path:
    work_dir = start_dir or Path().absolute()
    root_dir = root_dir or Path(work_dir.root)
    while work_dir != root_dir:
        potential = work_dir / name
        if potential.exists():
            return potential
        work_dir = work_dir.parent


class Variable(NamedTuple):
    key: str
    val: str

    @staticmethod
    def build_pattern() -> Pattern:
        return re.compile('^\s*"?(?P<key>[-.\w]+)"?\s*=\s*"?(?P<val>[-.\w]+)"?\s*(\Z|#.*)$')


def parse_config(path: Path) -> Iterator[Variable]:
    pattern = Variable.build_pattern()
    with path.open('r') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                yield Variable(**match.groupdict())


def load_config(path: Path) -> Dict[str, str]:
    return {var.key: var.val for var in parse_config(path)}


def main():
    parser = build_parser()
    args = parser.parse_args()
    name = f'{args.target}.{args.extension}'
    target = find_target(name)
    if not target:
        return
    data = load_config(target)
    print(data)

    here = Path().absolute()
    construct = here.relative_to(target.parent)
    print(construct)
