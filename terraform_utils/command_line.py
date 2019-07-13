from typing import Dict, Iterator, NamedTuple, Pattern
from argparse import ArgumentParser
from pathlib import Path, PurePosixPath
import re


def build_parser():
    parser = ArgumentParser()
    parser.add_argument('-t', '--target', type=str, default='common', help='tfvars search target')
    parser.add_argument('-k', '--key', type=str, help='variable to read')
    parser.add_argument('-c', '--component', choices=['bucket', 'object', 'table', 'env'])
    parser.add_argument('-x', '--extension', type=str, default='tfvars')
    parser.add_argument('--bucket-name', type=str, default='terraformstate')
    parser.add_argument('--table-name', type=str, default='terraformlock')
    parser.add_argument('--prefix', type=str, default='{app_name}-')
    parser.add_argument('--suffix', type=str, default='-{app_env}-{company}')
    parser.add_argument('--state-name', type=str, default='terraform.tfstate')
    parser.add_argument('--env-var', type=str, default='app_env')
    parser.add_argument('--env_pos', type=int, default=0)
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
        return re.compile('^\s*"?(?P<key>[-.\w]+)"?\s*=\s*"?(?P<val>[-.\w@]+)"?\s*(\Z|#.*)$')


def parse_config(path: Path) -> Iterator[Variable]:
    pattern = Variable.build_pattern()
    with path.open('r') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                yield Variable(**match.groupdict())


def load_config(path: Path) -> Dict[str, str]:
    return {var.key: var.val for var in parse_config(path)}


def infer_params(project_dir: Path, work_dir: Path = None,
                 app_env_var: str = 'app_env', app_env_pos: int = 0,
                 construct_var: str = 'construct') -> Dict[str, str]:
    work_dir = work_dir or Path().absolute()
    rel_path = work_dir.relative_to(project_dir)
    construct_parts = list(rel_path.parts)
    return {
        app_env_var: construct_parts.pop(app_env_pos),
        construct_var: str(Path(*construct_parts))
    }


def build_output(data: Dict[str, str], key: str = None, component: str = None,
                 prefix: str = '{app_name}-', suffix: str = '-{app_env}-{company}',
                 bucket_name: str = 'terraformstate', table_name: str = 'terraformlock',
                 state_name: str = 'terraform.tfstate', app_env_var: str = 'app_env') -> str:

    if key:
        return data.get(key)

    if component == 'env':
        return data[app_env_var]

    if component == 'bucket':
        return prefix.format(**data) + bucket_name + suffix.format(**data)

    if component == 'table':
        return prefix.format(**data) + table_name + suffix.format(**data)

    if component == 'object':
        state_path = Path(data['construct']) / state_name
        state_path = PurePosixPath(state_path)
        return str(state_path)


def main():
    parser = build_parser()
    args = parser.parse_args()
    name = f'{args.target}.{args.extension}'
    target = find_target(name)
    if not target:
        return
    config_data = load_config(target)
    infer_data = infer_params(project_dir=target.parent, app_env_var=args.env_var, app_env_pos=args.env_pos)
    data = {**config_data, **infer_data}
    output = build_output(data, key=args.key, component=args.component, prefix=args.prefix, suffix=args.suffix,
                          bucket_name=args.bucket_name, table_name=args.table_name, state_name=args.state_name,
                          app_env_var=args.env_var)
    if output:
        print(output, end='')
