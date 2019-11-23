from .utils import find_target, infer_params, load_config
from argparse import ArgumentParser, Namespace
from .core import build_output
from pathlib import Path
from typing import Dict


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


def main():
    parser: ArgumentParser= build_parser()
    args: Namespace = parser.parse_args()
    name: str = f'{args.target}.{args.extension}'
    target: Path = find_target(name)
    if not target:
        return
    config_data: Dict[str, str] = load_config(target)
    infer_data: Dict[str, str] = infer_params(project_dir=target.parent, app_env_var=args.env_var, app_env_pos=args.env_pos)
    data: Dict[str, str] = {**config_data, **infer_data}
    output: str = build_output(data, key=args.key, component=args.component, prefix=args.prefix, suffix=args.suffix,
                               bucket_name=args.bucket_name, table_name=args.table_name, state_name=args.state_name,
                               app_env_var=args.env_var)
    if output:
        print(output, end='')
