from pathlib import Path, PurePosixPath
from typing import Dict


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
