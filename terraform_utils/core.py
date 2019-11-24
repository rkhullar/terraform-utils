from typing import Dict, List, Optional, Union
from pathlib import Path, PurePosixPath

__all__ = ['infer_params', 'build_output', 'setup_project']


def infer_params(project_dir: Path, work_dir: Path = None, construct_var: str = 'construct',
                 app_env_var: str = 'app_env', app_env_pos: int = 0) -> Dict[str, str]:
    work_dir: Path = work_dir or Path().absolute()
    relative_path: Path = work_dir.relative_to(project_dir)
    construct_parts = list(relative_path.parts)
    return {app_env_var: construct_parts.pop(app_env_pos), construct_var: str(Path(*construct_parts))}


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


def setup_project(path: Optional[Union[Path, str]], create: bool = True,
                  constructs: List[str] = None, envs: List[str] = None,
                  common_name: str = 'common', common_ext: str = 'tfvars',
                  terragrunt_name: str = 'terragrunt', terragrunt_ext: str = 'hcl'):

    live_dir: Union[Path, str] = path or Path()
    live_dir: Path = Path(live_dir)
    live_dir.mkdir(exist_ok=create)

    envs = envs or ['sbx', 'dev', 'qa', 'uat', 'prd']
    constructs = constructs or ['params', 'network', 'iam', 'app']

    for env in envs:
        for construct in constructs:
            terragrunt_hcl = live_dir / env / construct / f'{terragrunt_name}.{terragrunt_ext}'
            terragrunt_hcl.parent.mkdir(exist_ok=True, parents=True)
            terragrunt_hcl.touch(exist_ok=True)

    terragrunt_hcl = live_dir / f'{terragrunt_name}.{terragrunt_ext}'
    common_tfvars = live_dir / f'{common_name}.{common_ext}'

    terragrunt_hcl.touch(exist_ok=True)
    common_tfvars.touch(exist_ok=True)
