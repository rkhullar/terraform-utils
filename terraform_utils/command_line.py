from argparse import ArgumentParser
from pathlib import Path


def build_parser():
    parser = ArgumentParser()
    parser.add_argument('-t', '--target', type=str, default='common', help='tfvars search target')
    parser.add_argument('-k', '--key', type=str, help='variable to read')
    parser.add_argument('-c', '--component', choices=['bucket', 'object', 'table', 'env'])
    parser.add_argument('-x', '--extension', type=str, default='tfvars')
    return parser


def find_target(name: str, start_dir: Path = None, root_dir: Path = None) -> Path:
    work_dir = start_dir or Path().absolute()
    root_dir = root_dir or Path(work_dir.root)
    while work_dir != root_dir:
        potential = work_dir / name
        if potential.exists():
            return potential
        work_dir = work_dir.parent


def main():
    parser = build_parser()
    args = parser.parse_args()
    name = f'{args.target}.{args.extension}'
    target = find_target(name)
    print(target)
